# app.py
"""
Main entry point for Investment Planner
Modular structure for efficient development
"""
import streamlit as st

# Import configuration
from config import APP_TITLE, APP_ICON, LAYOUT, CURRENCIES, CALCULATOR_MODES

# Import styles
from styles.custom_css import get_custom_css

# Import components
from components.hero import create_hero_section

# Configure page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Display hero section
st.markdown(create_hero_section(), unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h3 style='font-size:30px;font-weight: 700; color:rgba(255,255,255,0.95);'>🎛️ Controls</h3>", unsafe_allow_html=True)
currency = st.sidebar.selectbox("💱 Currency", CURRENCIES, help="Select your preferred currency")
mode = st.sidebar.selectbox("📊 Calculator Mode", CALCULATOR_MODES, help="Choose the calculator you want to use")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: left; padding: 1rem 0; color: rgba(255,255,255,0.9);'>
    <p style='font-size: 0.875rem; margin-bottom: 0.5rem;'><strong>💡 Quick Tips</strong></p>
    <p style='font-size: 0.75rem; line-height: 1.6;'>
    • Use sliders for quick adjustments<br/>
    • Enable inflation adjustment for realistic projections<br/>
    • Try different scenarios to find your optimal strategy
    </p>
</div>
""", unsafe_allow_html=True)

# Route to appropriate calculator page
# IMPORTANT: Changed 'pages' to 'views' to avoid Streamlit auto-navigation
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
<div style="text-align: center; color: var(--text-secondary); padding: 2rem 0;">
    <p style="margin-bottom: 0.5rem; font-size: 1rem;"><strong>💰 Investment Planner</strong> - Your Financial Future, Simplified</p>
    <p style="font-size: 0.875rem; opacity: 0.8;">Accurate calculations • Transparent methodology • Trusted by investors</p>
    <p style="font-size: 0.75rem; margin-top: 1rem; opacity: 0.6;">Phase 1 - Modular Architecture</p>
</div>
""", unsafe_allow_html=True)