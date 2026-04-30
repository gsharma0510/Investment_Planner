# views/sip_calculator.py
"""
SIP Calculator UI Page
"""
import streamlit as st
from config import DEFAULTS, RANGES, CONTRIBUTION_TIMING, SS
from calculators.sip import simulate_sip
from calculators.helpers import format_currency_str
from components.metrics import metric_card
from components.charts import create_line_chart


YEAR_TABLE_COLUMNS = {
    "year":                "Year",
    "begin_balance":       "Opening Balance",
    "annual_contribution": "Annual Investment",
    "interest_earned":     "Returns Earned",
    "end_balance":         "Closing Balance",
}


def render_sip_calculator(currency):
    """Render the SIP Calculator page."""

    st.markdown("## \U0001f4c8 SIP Calculator")
    st.markdown("Calculate your Systematic Investment Plan returns with step-up and inflation adjustment")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### \U0001f4b5 Investment Details")

        monthly_sip_col1, monthly_sip_col2 = st.columns([3, 1])
        SK = SS["sip_amount_slider"]
        IK = SS["sip_amount_input"]
        VK = SS["sip_amount"]

        if VK not in st.session_state:
            st.session_state[VK] = DEFAULTS['sip']['monthly_amount']
        if SK not in st.session_state:
            st.session_state[SK] = st.session_state[VK]
        if IK not in st.session_state:
            st.session_state[IK] = st.session_state[VK]

        def sync_from_slider():
            st.session_state[VK] = st.session_state[SK]
            st.session_state[IK] = st.session_state[VK]

        def sync_from_input():
            st.session_state[VK] = st.session_state[IK]
            st.session_state[SK] = st.session_state[VK]

        with monthly_sip_col1:
            st.slider(
                "Monthly SIP Amount",
                min_value=RANGES['monthly_sip']['min'],
                max_value=RANGES['monthly_sip']['max'],
                step=RANGES['monthly_sip']['step'],
                help="Slide to adjust your monthly investment amount",
                key=SK,
                on_change=sync_from_slider,
            )
        with monthly_sip_col2:
            st.number_input(
                "Manual",
                min_value=RANGES['monthly_sip']['min'],
                max_value=RANGES['monthly_sip']['max'],
                step=RANGES['monthly_sip']['step'],
                key=IK,
                label_visibility="collapsed",
                on_change=sync_from_input,
            )

        monthly_sip = st.session_state[VK]
        st.markdown(f"**{format_currency_str(currency, monthly_sip)}/month**")

        annual_return_pct = st.slider(
            "Expected Annual Return (%)",
            min_value=RANGES['annual_return']['min'],
            max_value=RANGES['annual_return']['max'],
            value=DEFAULTS['sip']['annual_return'],
            step=RANGES['annual_return']['step'],
            help="Expected average annual return on your investment",
        )
        years = st.slider(
            "Investment Duration (Years)",
            min_value=RANGES['years']['min'],
            max_value=RANGES['years']['max'],
            value=DEFAULTS['sip']['years'],
            step=RANGES['years']['step'],
            help="How long you plan to invest",
        )
        step_up_pct = st.slider(
            "Annual Step-Up (%)",
            min_value=RANGES['step_up']['min'],
            max_value=RANGES['step_up']['max'],
            value=DEFAULTS['sip']['step_up'],
            step=RANGES['step_up']['step'],
            help="Annual increase in your SIP amount",
        )

    with col2:
        st.markdown("#### \u2699\ufe0f Advanced Options")

        use_inflation = st.checkbox(
            "\U0001f504 Adjust contributions for inflation",
            value=False,
            help="Your contributions increase by the inflation rate each year to maintain purchasing power",
        )
        inflation_pct = st.slider(
            "Inflation Rate (%)",
            min_value=RANGES['inflation']['min'],
            max_value=RANGES['inflation']['max'],
            value=DEFAULTS['sip']['inflation'],
            step=RANGES['inflation']['step'],
            help="Expected average annual inflation rate",
        )
        payment_type = st.selectbox(
            "Contribution Timing",
            CONTRIBUTION_TIMING,
            help="Invest at the beginning or end of each month",
        )
        show_table = st.checkbox("\U0001f4ca Show yearly breakdown table", value=True)

    if use_inflation:
        st.info(
            "\U0001f4a1 With inflation adjustment enabled, your monthly contribution increases each year "
            "by the inflation rate to maintain purchasing power, on top of any step-up percentage."
        )

    # ── Calculations ──────────────────────────────────────────────────────────
    annual_return = annual_return_pct / 100.0
    step_up       = step_up_pct / 100.0
    inflation     = inflation_pct / 100.0
    contrib_begin = (payment_type == "Beginning")

    df_monthly, df_year, fv_nominal, fv_real, total_invested_nominal, total_invested_real = simulate_sip(
        monthly_sip, annual_return, years, step_up, use_inflation, inflation, contrib_begin
    )

    est_return_nom  = fv_nominal - total_invested_nominal
    est_return_real = fv_real    - total_invested_real
    overall_return_nom_pct  = (est_return_nom  / total_invested_nominal * 100) if total_invested_nominal else 0.0
    overall_return_real_pct = (est_return_real / total_invested_real    * 100) if total_invested_real    else 0.0

    # ── Results ───────────────────────────────────────────────────────────────
    st.markdown("### \U0001f4ca Summary Metrics")
    cols = st.columns(4)
    cols[0].markdown(metric_card("Total Invested",    format_currency_str(currency, total_invested_nominal)), unsafe_allow_html=True)
    cols[1].markdown(metric_card("Final Corpus",      format_currency_str(currency, fv_nominal),   f"+{overall_return_nom_pct:.0f}%", "positive"), unsafe_allow_html=True)
    cols[2].markdown(metric_card("Estimated Returns", format_currency_str(currency, est_return_nom), "Nominal", "neutral"), unsafe_allow_html=True)
    cols[3].markdown(metric_card("Overall Gain",      f"{overall_return_nom_pct:.1f}%", "Nominal", "positive"), unsafe_allow_html=True)

    if use_inflation:
        st.markdown("#### \U0001f48e Inflation-Adjusted (Today's Value)")
        cols = st.columns(4)
        cols[0].markdown(metric_card("Total Invested",    format_currency_str(currency, total_invested_real),   "Real Value", "neutral"), unsafe_allow_html=True)
        cols[1].markdown(metric_card("Final Corpus",      format_currency_str(currency, fv_real),               f"+{overall_return_real_pct:.0f}%", "positive"), unsafe_allow_html=True)
        cols[2].markdown(metric_card("Estimated Returns", format_currency_str(currency, est_return_real),        "Real", "neutral"), unsafe_allow_html=True)
        cols[3].markdown(metric_card("Overall Gain",      f"{overall_return_real_pct:.1f}%",                    "Real", "positive"), unsafe_allow_html=True)

    st.markdown("### \U0001f4c8 Growth Over Time")
    fig = create_line_chart(df_monthly, currency, inflation, use_inflation)
    st.plotly_chart(fig, use_container_width=True)

    if show_table:
        st.markdown("### \U0001f4cb Year-by-Year Breakdown")
        display_df = (
            df_year[list(YEAR_TABLE_COLUMNS.keys())]
            .round(0)
            .rename(columns=YEAR_TABLE_COLUMNS)
        )
        st.dataframe(display_df, use_container_width=True, height=400)