# views/swp_calculator.py
"""
SWP Calculator UI Page
"""
import streamlit as st
from config import DEFAULTS, RANGES, SS
from calculators.swp import simulate_swp, max_sustainable_withdrawal
from calculators.helpers import format_currency_str
from components.metrics import metric_card
from components.charts import create_swp_chart


YEAR_TABLE_COLUMNS = {
    "year":               "Year",
    "begin_balance":      "Opening Balance",
    "annual_withdrawal":  "Annual Withdrawal",
    "interest_earned":    "Returns Earned",
    "end_balance":        "Closing Balance",
}


def render_swp_calculator(currency):
    """Render the SWP Calculator page."""

    st.markdown("## \U0001f4b8 SWP Calculator")
    st.markdown("Plan your Systematic Withdrawal for retirement with step-up options")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### \U0001f4b0 Corpus Details")

        corpus_col1, corpus_col2 = st.columns([3, 1])
        SK = SS["swp_corpus_slider"]
        IK = SS["swp_corpus_input"]
        VK = SS["swp_corpus"]

        if VK not in st.session_state:
            st.session_state[VK] = DEFAULTS['swp']['initial_corpus']
        if SK not in st.session_state:
            st.session_state[SK] = st.session_state[VK]
        if IK not in st.session_state:
            st.session_state[IK] = st.session_state[VK]

        def sync_corpus_slider():
            st.session_state[VK] = st.session_state[SK]
            st.session_state[IK] = st.session_state[VK]

        def sync_corpus_input():
            st.session_state[VK] = st.session_state[IK]
            st.session_state[SK] = st.session_state[VK]

        with corpus_col1:
            st.slider(
                "Initial Corpus",
                min_value=RANGES['initial_corpus']['min'],
                max_value=RANGES['initial_corpus']['max'],
                step=RANGES['initial_corpus']['step'],
                help="Your retirement corpus at the start",
                key=SK,
                on_change=sync_corpus_slider,
            )
        with corpus_col2:
            st.number_input(
                "Manual",
                min_value=RANGES['initial_corpus']['min'],
                max_value=RANGES['initial_corpus']['max'],
                step=RANGES['initial_corpus']['step'],
                key=IK,
                label_visibility="collapsed",
                on_change=sync_corpus_input,
            )

        initial_corpus = st.session_state[VK]
        st.markdown(f"**{format_currency_str(currency, initial_corpus)}**")

        annual_return_pct = st.slider(
            "Expected Annual Return (%)",
            min_value=RANGES['annual_return']['min'],
            max_value=RANGES['annual_return']['max'],
            value=DEFAULTS['swp']['annual_return'],
            step=RANGES['annual_return']['step'],
            help="Expected average annual return on remaining corpus",
        )
        years = st.slider(
            "Plan Duration (Years)",
            min_value=RANGES['swp_years']['min'],
            max_value=RANGES['swp_years']['max'],
            value=DEFAULTS['swp']['years'],
            step=RANGES['swp_years']['step'],
            help="How long you want the corpus to last",
        )

    with col2:
        st.markdown("#### \U0001f4b5 Withdrawal Details")

        withdrawal_col1, withdrawal_col2 = st.columns([3, 1])
        SKW = SS["swp_withdrawal_slider"]
        IKW = SS["swp_withdrawal_input"]
        VKW = SS["swp_withdrawal"]

        if VKW not in st.session_state:
            st.session_state[VKW] = DEFAULTS['swp']['monthly_withdrawal']
        if SKW not in st.session_state:
            st.session_state[SKW] = st.session_state[VKW]
        if IKW not in st.session_state:
            st.session_state[IKW] = st.session_state[VKW]

        def sync_withdrawal_slider():
            st.session_state[VKW] = st.session_state[SKW]
            st.session_state[IKW] = st.session_state[VKW]

        def sync_withdrawal_input():
            st.session_state[VKW] = st.session_state[IKW]
            st.session_state[SKW] = st.session_state[VKW]

        with withdrawal_col1:
            st.slider(
                "Monthly Withdrawal",
                min_value=RANGES['monthly_withdrawal']['min'],
                max_value=RANGES['monthly_withdrawal']['max'],
                step=RANGES['monthly_withdrawal']['step'],
                help="Amount you want to withdraw each month",
                key=SKW,
                on_change=sync_withdrawal_slider,
            )
        with withdrawal_col2:
            st.number_input(
                "Manual",
                min_value=RANGES['monthly_withdrawal']['min'],
                max_value=RANGES['monthly_withdrawal']['max'],
                step=RANGES['monthly_withdrawal']['step'],
                key=IKW,
                label_visibility="collapsed",
                on_change=sync_withdrawal_input,
            )

        monthly_withdrawal = st.session_state[VKW]
        st.markdown(f"**{format_currency_str(currency, monthly_withdrawal)}/month**")

        step_up_pct = st.slider(
            "Annual Step-Up (%)",
            min_value=RANGES['step_up']['min'],
            max_value=RANGES['step_up']['max'],
            value=DEFAULTS['swp']['step_up'],
            step=RANGES['step_up']['step'],
            help="Annual increase in withdrawal to counter inflation",
        )
        use_inflation = st.checkbox("Show inflation-adjusted final corpus?", value=False)
        inflation_pct = st.slider(
            "Inflation (%)",
            min_value=RANGES['inflation']['min'],
            max_value=RANGES['inflation']['max'],
            value=DEFAULTS['swp']['inflation'],
            step=RANGES['inflation']['step'],
        )
        show_table = st.checkbox("\U0001f4ca Show yearly table", value=True)

    # ── Calculations ──────────────────────────────────────────────────────────
    annual_return = annual_return_pct / 100.0
    step_up       = step_up_pct / 100.0
    inflation     = inflation_pct / 100.0

    max_withdrawal = max_sustainable_withdrawal(initial_corpus, annual_return, years)
    st.info(f"\U0001f4a1 Max sustainable monthly withdrawal \u2248 {format_currency_str(currency, max_withdrawal)}")

    df_monthly,         df_year,         exhausted_month    = simulate_swp(initial_corpus, annual_return, years, monthly_withdrawal, step_up, use_inflation, inflation)
    df_monthly_no_step, df_year_no_step, exhausted_month_no = simulate_swp(initial_corpus, annual_return, years, monthly_withdrawal, 0.0,     use_inflation, inflation)

    end_balance         = df_year["end_balance"].iloc[-1]
    end_balance_no      = df_year_no_step["end_balance"].iloc[-1]
    end_balance_real    = end_balance    / ((1 + inflation) ** years) if inflation > 0 else end_balance
    end_balance_no_real = end_balance_no / ((1 + inflation) ** years) if inflation > 0 else end_balance_no

    # ── Exhaustion warnings ───────────────────────────────────────────────────
    if exhausted_month and exhausted_month_no:
        st.error("\u26a0\ufe0f Corpus exhausted in both scenarios!")
        st.warning(f"\u2022 **Without Step-Up**: Funds run out in {exhausted_month_no.strftime('%b %Y')}")
        st.warning(f"\u2022 **With Step-Up**: Funds run out in {exhausted_month.strftime('%b %Y')}")
    elif exhausted_month and not exhausted_month_no:
        st.warning(f"\u26a0\ufe0f **With Step-Up**: Corpus exhausted in {exhausted_month.strftime('%b %Y')}")
        st.info("\u2714 Without step-up, the corpus survives the full duration")
    elif exhausted_month_no and not exhausted_month:
        st.warning(f"\u26a0\ufe0f **Without Step-Up**: Corpus exhausted in {exhausted_month_no.strftime('%b %Y')}")
        st.success("\u2714 With step-up, the corpus survives the full duration")

    # ── Results ───────────────────────────────────────────────────────────────
    st.markdown("### \U0001f4ca Ending Balance")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(metric_card("Without Step-Up", format_currency_str(currency, end_balance_no), "Nominal", "neutral"), unsafe_allow_html=True)
        if use_inflation:
            st.markdown(metric_card("Without Step-Up", format_currency_str(currency, end_balance_no_real), "Inflation Adjusted", "neutral"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("With Step-Up", format_currency_str(currency, end_balance), "Nominal", "neutral"), unsafe_allow_html=True)
        if use_inflation:
            st.markdown(metric_card("With Step-Up", format_currency_str(currency, end_balance_real), "Inflation Adjusted", "neutral"), unsafe_allow_html=True)

    st.markdown("### \U0001f4c9 Corpus Over Time")
    fig = create_swp_chart(df_monthly_no_step, df_monthly, currency)
    st.plotly_chart(fig, use_container_width=True)

    if show_table:
        st.markdown("### \U0001f4cb Year-by-Year Summary (With Step-Up)")
        display_df = (
            df_year[list(YEAR_TABLE_COLUMNS.keys())]
            .round(0)
            .rename(columns=YEAR_TABLE_COLUMNS)
        )
        st.dataframe(display_df, use_container_width=True, height=400)