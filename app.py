# app.py
"""
Main entry point for Investment Planner
"""
import streamlit as st

from config import APP_TITLE, APP_ICON, LAYOUT, CURRENCIES, CALCULATOR_MODES
from styles.custom_css import get_custom_css
from components.hero import create_hero_section

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
st.markdown(create_hero_section(), unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown(
    "<h3 style='font-size:30px; font-weight:700; color:rgba(255,255,255,0.95);'>\U0001f39b\ufe0f Controls</h3>",
    unsafe_allow_html=True,
)
currency = st.sidebar.selectbox("\U0001f4b1 Currency", CURRENCIES, help="Select your preferred currency")
mode     = st.sidebar.selectbox("\U0001f4ca Calculator Mode", CALCULATOR_MODES, help="Choose the calculator you want to use")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align:left; padding:1rem 0; color:rgba(255,255,255,0.9);'>
    <p style='font-size:0.875rem; margin-bottom:0.5rem;'><strong>\U0001f4a1 Quick Tips</strong></p>
    <p style='font-size:0.75rem; line-height:1.6;'>
    &bull; Use sliders for quick adjustments<br/>
    &bull; Enable inflation adjustment for realistic projections<br/>
    &bull; Try different scenarios to find your optimal strategy
    </p>
</div>
""", unsafe_allow_html=True)

# Route to calculator
if mode == "SIP Calculator":
    from views.sip_calculator import render_sip_calculator
    render_sip_calculator(currency)

elif mode == "SWP Calculator":
    from views.swp_calculator import render_swp_calculator
    render_swp_calculator(currency)

elif mode == "Retirement Planner":
    from views.retirement_planner import render_retirement_planner
    render_retirement_planner(currency)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:var(--text-secondary); padding:2rem 0;">
    <p style="margin-bottom:0.5rem; font-size:1rem;"><strong>\U0001f4b0 Investment Planner</strong> - Your Financial Future, Simplified</p>
    <p style="font-size:0.875rem; opacity:0.8;">Accurate calculations &bull; Transparent methodology &bull; Trusted by investors</p>
    <p style="font-size:0.75rem; margin-top:1rem; opacity:0.6;">Phase 1 - Modular Architecture</p>
</div>
""", unsafe_allow_html=True)