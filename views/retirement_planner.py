# views/retirement_planner.py
"""
Retirement Back-Calculator UI Page - FIXED VERSION with proper slider-input sync
"""
import streamlit as st
from config import DEFAULTS, RANGES, CONTRIBUTION_TIMING
from calculators.sip import simulate_sip, find_required_monthly_sip
from calculators.helpers import format_currency_str
from components.metrics import metric_card
from components.charts import create_retirement_chart


def render_retirement_planner(currency):
    """Render the Retirement Goal Calculator page"""

    st.markdown("## 🎯 Retirement Goal Calculator")
    st.markdown("Find the exact monthly SIP needed to reach your retirement goal")

    # Input Section
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 👤 Personal Details")
        current_age = st.slider(
            "Current Age",
            min_value=RANGES['age']['min'],
            max_value=65,
            value=DEFAULTS['retirement']['current_age'],
            step=RANGES['age']['step']
        )
        retirement_age = st.slider(
            "Retirement Age",
            min_value=40,
            max_value=RANGES['age']['max'],
            value=DEFAULTS['retirement']['retirement_age'],
            step=RANGES['age']['step']
        )

        st.markdown("#### 🎯 Financial Goal")

        # --- Retirement Goal with slider + manual input (synchronized) ---
        goal_col1, goal_col2 = st.columns([3, 1])

        slider_key = "retirement_goal_slider"
        input_key = "retirement_goal_input"

        # --- Initialize session state once ---
        if "target_goal" not in st.session_state:
            st.session_state.target_goal = DEFAULTS['retirement']['target_goal']
        if slider_key not in st.session_state:
            st.session_state[slider_key] = st.session_state.target_goal
        if input_key not in st.session_state:
            st.session_state[input_key] = st.session_state.target_goal

        # --- Sync Functions ---
        def sync_from_slider():
            st.session_state.target_goal = st.session_state[slider_key]
            st.session_state[input_key] = st.session_state.target_goal

        def sync_from_input():
            st.session_state.target_goal = st.session_state[input_key]
            st.session_state[slider_key] = st.session_state.target_goal

        # --- Widgets ---
        with goal_col1:
            st.slider(
                "Retirement Goal",
                min_value=RANGES['retirement_goal']['min'],
                max_value=RANGES['retirement_goal']['max'],
                step=RANGES['retirement_goal']['step'],
                help="Target corpus you want at retirement",
                key=slider_key,
                on_change=sync_from_slider,
            )

        with goal_col2:
            st.number_input(
                "Manual",
                min_value=RANGES['retirement_goal']['min'],
                max_value=RANGES['retirement_goal']['max'],
                step=RANGES['retirement_goal']['step'],
                key=input_key,
                label_visibility="collapsed",
                on_change=sync_from_input,
            )

        # --- Unified synced value ---
        target_goal = st.session_state.target_goal
        st.markdown(f"**{format_currency_str(currency, target_goal)}**")

        annual_return_pct = st.slider(
            "Expected Annual Return (%)",
            min_value=RANGES['annual_return']['min'],
            max_value=25.0,
            value=DEFAULTS['retirement']['annual_return'],
            step=RANGES['annual_return']['step']
        )

    with col2:
        st.markdown("#### ⚙️ Strategy")
        step_up_pct = st.slider(
            "Annual SIP Step-Up (%)",
            min_value=RANGES['step_up']['min'],
            max_value=RANGES['step_up']['max'],
            value=DEFAULTS['retirement']['step_up'],
            step=RANGES['step_up']['step']
        )

        use_inflation = st.checkbox(
            "Target is in today's value (inflation-adjusted)?",
            value=True,
            help="If checked, the target will be adjusted for inflation"
        )
        inflation_pct = st.slider(
            "Inflation (%)",
            min_value=RANGES['inflation']['min'],
            max_value=RANGES['inflation']['max'],
            value=DEFAULTS['retirement']['inflation'],
            step=RANGES['inflation']['step']
        )

        payment_type = st.selectbox("Contribution Timing", CONTRIBUTION_TIMING)

        st.markdown("#### 📊 Timeline")
        years = int(retirement_age - current_age)
        st.info(f"⏱️ Investment Duration: **{years} years**")

    # Calculate
    annual_return = annual_return_pct / 100.0
    step_up = step_up_pct / 100.0
    inflation = inflation_pct / 100.0
    contrib_begin = (payment_type == "Beginning")

    if st.button("🚀 Calculate Required Monthly SIP", use_container_width=True):
        with st.spinner("Calculating your personalized investment plan..."):
            required_sip = find_required_monthly_sip(
                target_goal, annual_return, years, step_up, use_inflation, inflation, contrib_begin
            )
            df_monthly, df_year, fv_nom, fv_real, total_invested_nom, total_invested_real = simulate_sip(
                required_sip, annual_return, years, step_up, use_inflation, inflation, contrib_begin
            )

        st.success(f"✅ **Required Monthly SIP:** {format_currency_str(currency, required_sip)}")

        # Display Results
        st.markdown("### 📊 Investment Summary")
        cols = st.columns(3)
        cols[0].markdown(
            metric_card("Starting SIP", format_currency_str(currency, required_sip), "Per Month", "positive"),
            unsafe_allow_html=True)
        cols[1].markdown(
            metric_card("Total Investment", format_currency_str(currency, total_invested_nom), "Nominal", "neutral"),
            unsafe_allow_html=True)
        if use_inflation:
            cols[2].markdown(
                metric_card("Total Investment", format_currency_str(currency, total_invested_real), "Today's Value",
                            "neutral"), unsafe_allow_html=True)
        else:
            cols[2].markdown(
                metric_card("Final Corpus", format_currency_str(currency, fv_nom), "Projected", "positive"),
                unsafe_allow_html=True)

        # Chart
        st.markdown("### 📈 Projected Growth")
        fig = create_retirement_chart(df_monthly, target_goal, currency)
        st.plotly_chart(fig, use_container_width=True)

        # Table
        st.markdown("### 📋 Yearly Breakdown")
        st.dataframe(
            df_year[["year", "begin_balance", "annual_contribution", "interest_earned", "end_balance"]].round(0),
            use_container_width=True,
            height=400
        )