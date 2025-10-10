# views/swp_calculator.py
"""
SWP Calculator UI Page - FIXED VERSION with proper slider-input sync
"""
import streamlit as st
from config import DEFAULTS, RANGES
from calculators.swp import simulate_swp, max_sustainable_withdrawal
from calculators.helpers import format_currency_str
from components.metrics import metric_card
from components.charts import create_swp_chart


def render_swp_calculator(currency):
    """Render the SWP Calculator page"""

    st.markdown("## 💸 SWP Calculator")
    st.markdown("Plan your Systematic Withdrawal for retirement with step-up options")

    # Input Section
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 💰 Corpus Details")

        # --- Initial Corpus with slider + manual input (synchronized) ---
        corpus_col1, corpus_col2 = st.columns([3, 1])

        slider_key = "initial_corpus_slider"
        input_key = "initial_corpus_input"

        # --- Initialize session state values once ---
        if "initial_corpus" not in st.session_state:
            st.session_state.initial_corpus = DEFAULTS['swp']['initial_corpus']
        if slider_key not in st.session_state:
            st.session_state[slider_key] = st.session_state.initial_corpus
        if input_key not in st.session_state:
            st.session_state[input_key] = st.session_state.initial_corpus

        # --- Sync Functions ---
        def sync_from_slider():
            st.session_state.initial_corpus = st.session_state[slider_key]
            st.session_state[input_key] = st.session_state.initial_corpus

        def sync_from_input():
            st.session_state.initial_corpus = st.session_state[input_key]
            st.session_state[slider_key] = st.session_state.initial_corpus

        # --- Widgets ---
        with corpus_col1:
            st.slider(
                "Initial Corpus",
                min_value=RANGES['initial_corpus']['min'],
                max_value=RANGES['initial_corpus']['max'],
                step=RANGES['initial_corpus']['step'],
                help="Your retirement corpus at the start",
                key=slider_key,
                on_change=sync_from_slider,
            )

        with corpus_col2:
            st.number_input(
                "Manual",
                min_value=RANGES['initial_corpus']['min'],
                max_value=RANGES['initial_corpus']['max'],
                step=RANGES['initial_corpus']['step'],
                key=input_key,
                label_visibility="collapsed",
                on_change=sync_from_input,
            )

        # --- Unified synced value ---
        initial_corpus = st.session_state.initial_corpus
        st.markdown(f"**{format_currency_str(currency, initial_corpus)}**")

        annual_return_pct = st.slider(
            "Expected Annual Return (%)",
            min_value=RANGES['annual_return']['min'],
            max_value=RANGES['annual_return']['max'],
            value=DEFAULTS['swp']['annual_return'],
            step=RANGES['annual_return']['step'],
            help="Expected average annual return on remaining corpus"
        )

        years = st.slider(
            "Plan Duration (Years)",
            min_value=RANGES['swp_years']['min'],
            max_value=RANGES['swp_years']['max'],
            value=DEFAULTS['swp']['years'],
            step=RANGES['swp_years']['step'],
            help="How long you want the corpus to last"
        )

    with col2:
        st.markdown("#### 💵 Withdrawal Details")

        # --- Monthly Withdrawal with slider + manual input (synchronized) ---
        withdrawal_col1, withdrawal_col2 = st.columns([3, 1])

        slider_key_w = "monthly_withdrawal_slider"
        input_key_w = "monthly_withdrawal_input"

        # --- Initialize session state values once ---
        if "monthly_withdrawal" not in st.session_state:
            st.session_state.monthly_withdrawal = DEFAULTS['swp']['monthly_withdrawal']
        if slider_key_w not in st.session_state:
            st.session_state[slider_key_w] = st.session_state.monthly_withdrawal
        if input_key_w not in st.session_state:
            st.session_state[input_key_w] = st.session_state.monthly_withdrawal

        # --- Sync Functions ---
        def sync_from_slider_w():
            st.session_state.monthly_withdrawal = st.session_state[slider_key_w]
            st.session_state[input_key_w] = st.session_state.monthly_withdrawal

        def sync_from_input_w():
            st.session_state.monthly_withdrawal = st.session_state[input_key_w]
            st.session_state[slider_key_w] = st.session_state.monthly_withdrawal

        # --- Widgets ---
        with withdrawal_col1:
            st.slider(
                "Monthly Withdrawal",
                min_value=RANGES['monthly_withdrawal']['min'],
                max_value=RANGES['monthly_withdrawal']['max'],
                step=RANGES['monthly_withdrawal']['step'],
                help="Amount you want to withdraw each month",
                key=slider_key_w,
                on_change=sync_from_slider_w,
            )

        with withdrawal_col2:
            st.number_input(
                "Manual",
                min_value=RANGES['monthly_withdrawal']['min'],
                max_value=RANGES['monthly_withdrawal']['max'],
                step=RANGES['monthly_withdrawal']['step'],
                key=input_key_w,
                label_visibility="collapsed",
                on_change=sync_from_input_w,
            )

        # --- Unified synced value ---
        monthly_withdrawal = st.session_state.monthly_withdrawal
        st.markdown(f"**{format_currency_str(currency, monthly_withdrawal)}/month**")

        step_up_pct = st.slider(
            "Annual Step-Up (%)",
            min_value=RANGES['step_up']['min'],
            max_value=RANGES['step_up']['max'],
            value=DEFAULTS['swp']['step_up'],
            step=RANGES['step_up']['step'],
            help="Annual increase in withdrawal to counter inflation"
        )

        use_inflation = st.checkbox("Show inflation-adjusted final corpus?", value=False)
        inflation_pct = st.slider(
            "Inflation (%)",
            min_value=RANGES['inflation']['min'],
            max_value=RANGES['inflation']['max'],
            value=DEFAULTS['swp']['inflation'],
            step=RANGES['inflation']['step']
        )
        show_table = st.checkbox("📊 Show yearly table", value=True)

    # Calculate
    annual_return = annual_return_pct / 100.0
    step_up = step_up_pct / 100.0
    inflation = inflation_pct / 100.0

    max_withdrawal = max_sustainable_withdrawal(initial_corpus, annual_return, years)
    st.info(f"💡 Max sustainable monthly withdrawal ≈ {format_currency_str(currency, max_withdrawal)}")

    # Simulate with and without step-up
    df_monthly, df_year, exhausted_month = simulate_swp(
        initial_corpus, annual_return, years, monthly_withdrawal, step_up, use_inflation, inflation
    )
    df_monthly_no_step, df_year_no_step, exhausted_month_no = simulate_swp(
        initial_corpus, annual_return, years, monthly_withdrawal, 0.0, use_inflation, inflation
    )

    # Calculate ending balances
    end_balance = df_year["end_balance"].iloc[-1]
    end_balance_no = df_year_no_step["end_balance"].iloc[-1]
    end_balance_real = end_balance / ((1 + inflation) ** years) if inflation > 0 else end_balance
    end_balance_no_real = end_balance_no / ((1 + inflation) ** years) if inflation > 0 else end_balance_no

    # Conditional exhaustion warnings
    if exhausted_month and exhausted_month_no:
        st.error(f"⚠️ Corpus exhausted in both scenarios!")
        st.warning(f"• **Without Step-Up**: Funds run out in {exhausted_month_no.strftime('%b %Y')}")
        st.warning(f"• **With Step-Up**: Funds run out in {exhausted_month.strftime('%b %Y')}")
    elif exhausted_month and not exhausted_month_no:
        st.warning(f"⚠️ **With Step-Up**: Corpus exhausted in {exhausted_month.strftime('%b %Y')}")
        st.info("✓ Without step-up, the corpus survives the full duration")
    elif exhausted_month_no and not exhausted_month:
        st.warning(f"⚠️ **Without Step-Up**: Corpus exhausted in {exhausted_month_no.strftime('%b %Y')}")
        st.success("✓ With step-up, the corpus survives the full duration")

    # Display Results
    st.markdown("### 📊 Ending Balance Metrics")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(metric_card("Without Step-Up", format_currency_str(currency, end_balance_no), "Nominal", "neutral"),
                    unsafe_allow_html=True)
        if use_inflation:
            st.markdown(
                metric_card("Without Step-Up", format_currency_str(currency, end_balance_no_real), "Inflation Adjusted",
                            "neutral"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("With Step-Up", format_currency_str(currency, end_balance), "Nominal", "neutral"),
                    unsafe_allow_html=True)
        if use_inflation:
            st.markdown(
                metric_card("With Step-Up", format_currency_str(currency, end_balance_real), "Inflation Adjusted",
                            "neutral"), unsafe_allow_html=True)

    # Chart
    st.markdown("### 📉 Corpus Over Time")
    fig = create_swp_chart(df_monthly_no_step, df_monthly, currency)
    st.plotly_chart(fig, use_container_width=True)

    # Table
    if show_table:
        st.markdown("### 📋 Yearly Summary (With Step-Up)")
        st.dataframe(
            df_year[["year", "begin_balance", "annual_withdrawal", "interest_earned", "end_balance"]].round(0),
            use_container_width=True,
            height=400
        )