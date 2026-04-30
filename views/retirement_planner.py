# views/retirement_planner.py
"""
Retirement Back-Calculator UI Page
"""
import streamlit as st
from config import DEFAULTS, RANGES, CONTRIBUTION_TIMING, SS
from calculators.sip import simulate_sip, find_required_monthly_sip
from calculators.helpers import format_currency_str
from components.metrics import metric_card
from components.charts import create_retirement_chart


# Human-readable column headers for the yearly table
YEAR_TABLE_COLUMNS = {
    "year":                "Year",
    "begin_balance":       "Opening Balance",
    "annual_contribution": "Annual Investment",
    "interest_earned":     "Returns Earned",
    "end_balance":         "Closing Balance",
}


def render_retirement_planner(currency):
    """Render the Retirement Goal Calculator page."""

    st.markdown("## \U0001f3af Retirement Goal Calculator")
    st.markdown("Find the exact monthly SIP needed to reach your retirement goal")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### \U0001f464 Personal Details")

        current_age = st.slider(
            "Current Age",
            min_value=RANGES['age']['min'],
            max_value=65,
            value=DEFAULTS['retirement']['current_age'],
            step=RANGES['age']['step'],
        )
        retirement_age = st.slider(
            "Retirement Age",
            min_value=40,
            max_value=RANGES['age']['max'],
            value=DEFAULTS['retirement']['retirement_age'],
            step=RANGES['age']['step'],
        )

        years = int(retirement_age - current_age)
        if years <= 0:
            st.error(
                f"\u26a0\ufe0f Retirement age ({retirement_age}) must be greater than "
                f"your current age ({current_age}). Please adjust the sliders."
            )
            return

        st.markdown("#### \U0001f3af Financial Goal")

        goal_col1, goal_col2 = st.columns([3, 1])
        SK = SS["ret_goal_slider"]
        IK = SS["ret_goal_input"]
        VK = SS["ret_goal"]

        if VK not in st.session_state:
            st.session_state[VK] = DEFAULTS['retirement']['target_goal']
        if SK not in st.session_state:
            st.session_state[SK] = st.session_state[VK]
        if IK not in st.session_state:
            st.session_state[IK] = st.session_state[VK]

        def sync_goal_slider():
            st.session_state[VK] = st.session_state[SK]
            st.session_state[IK] = st.session_state[VK]

        def sync_goal_input():
            st.session_state[VK] = st.session_state[IK]
            st.session_state[SK] = st.session_state[VK]

        with goal_col1:
            st.slider(
                "Retirement Goal",
                min_value=RANGES['retirement_goal']['min'],
                max_value=RANGES['retirement_goal']['max'],
                step=RANGES['retirement_goal']['step'],
                help="Target corpus you want at retirement",
                key=SK,
                on_change=sync_goal_slider,
            )
        with goal_col2:
            st.number_input(
                "Manual",
                min_value=RANGES['retirement_goal']['min'],
                max_value=RANGES['retirement_goal']['max'],
                step=RANGES['retirement_goal']['step'],
                key=IK,
                label_visibility="collapsed",
                on_change=sync_goal_input,
            )

        target_goal = st.session_state[VK]
        st.markdown(f"**{format_currency_str(currency, target_goal)}**")

        annual_return_pct = st.slider(
            "Expected Annual Return (%)",
            min_value=RANGES['annual_return']['min'],
            max_value=25.0,
            value=DEFAULTS['retirement']['annual_return'],
            step=RANGES['annual_return']['step'],
        )

    with col2:
        st.markdown("#### \u2699\ufe0f Strategy")

        step_up_pct = st.slider(
            "Annual SIP Step-Up (%)",
            min_value=RANGES['step_up']['min'],
            max_value=RANGES['step_up']['max'],
            value=DEFAULTS['retirement']['step_up'],
            step=RANGES['step_up']['step'],
        )

        use_inflation = st.checkbox(
            "Target is in today's value (inflation-adjusted)?",
            value=True,
            help=(
                "ON: Your goal is in today's purchasing power. The calculator finds "
                "the SIP that delivers that real value after inflation is accounted for. "
                "OFF: Your goal is a fixed nominal amount at retirement."
            ),
        )
        inflation_pct = st.slider(
            "Inflation (%)",
            min_value=RANGES['inflation']['min'],
            max_value=RANGES['inflation']['max'],
            value=DEFAULTS['retirement']['inflation'],
            step=RANGES['inflation']['step'],
        )

        payment_type = st.selectbox("Contribution Timing", CONTRIBUTION_TIMING)

        st.markdown("#### \U0001f4ca Timeline")
        st.info(f"\u23f1\ufe0f Investment Duration: **{years} years**")

    # ── Calculations ──────────────────────────────────────────────────────────
    annual_return = annual_return_pct / 100.0
    step_up       = step_up_pct / 100.0
    inflation     = inflation_pct / 100.0
    contrib_begin = (payment_type == "Beginning")

    if st.button("\U0001f680 Calculate Required Monthly SIP", use_container_width=True):
        with st.spinner("Calculating your personalised investment plan..."):
            required_sip = find_required_monthly_sip(
                target_goal, annual_return, years, step_up,
                use_inflation, inflation, contrib_begin,
            )
            df_monthly, df_year, fv_nom, fv_real, total_invested_nom, total_invested_real = simulate_sip(
                required_sip, annual_return, years, step_up,
                use_inflation, inflation, contrib_begin,
            )

        st.success(f"\u2705 **Required Monthly SIP:** {format_currency_str(currency, required_sip)}")

        # ── Inflation context callout ──────────────────────────────────────
        if use_inflation:
            st.info(
                    f"💡 **How to read these numbers:** Your goal of " 
                    f"{format_currency_str(currency, target_goal)} is in *today's purchasing power*. "
                    f"After {years} years at {inflation_pct:.0f}% inflation, your corpus will grow to "
                    f"**{format_currency_str(currency, fv_nom)}** in nominal terms — "
                    f"but that larger amount buys exactly what "
                    f"{format_currency_str(currency, target_goal)} buys today."
            )

        # ── Summary metrics ───────────────────────────────────────────────
        st.markdown("### \U0001f4ca Investment Summary")
        cols = st.columns(3)

        cols[0].markdown(
            metric_card("Starting Monthly SIP", format_currency_str(currency, required_sip), "Per Month", "positive"),
            unsafe_allow_html=True,
        )
        cols[1].markdown(
            metric_card("Total Amount Invested", format_currency_str(currency, total_invested_nom), "Nominal", "neutral"),
            unsafe_allow_html=True,
        )
        if use_inflation:
            cols[2].markdown(
                metric_card("Total Invested", format_currency_str(currency, total_invested_real), "In Today's Value", "neutral"),
                unsafe_allow_html=True,
            )
        else:
            cols[2].markdown(
                metric_card("Final Corpus", format_currency_str(currency, fv_nom), "At Retirement", "positive"),
                unsafe_allow_html=True,
            )

        # ── Chart ─────────────────────────────────────────────────────────
        st.markdown("### \U0001f4c8 Projected Growth")
        # Show nominal corpus growth; goal line = nominal equivalent of the real target
        fig = create_retirement_chart(df_monthly, fv_nom if use_inflation else target_goal, currency)
        st.plotly_chart(fig, use_container_width=True)

        # ── Yearly table ──────────────────────────────────────────────────
        st.markdown("### \U0001f4cb Year-by-Year Breakdown")
        if use_inflation:
            st.caption(
                f"All figures are nominal (future rupees). "
                f"Divide any value by (1 + {inflation_pct:.0f}%)\u207f to get today's equivalent purchasing power."
            )

        display_df = (
            df_year[list(YEAR_TABLE_COLUMNS.keys())]
            .round(0)
            .rename(columns=YEAR_TABLE_COLUMNS)
        )
        st.dataframe(display_df, use_container_width=True, height=400)