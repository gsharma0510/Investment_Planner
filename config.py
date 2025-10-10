# config.py
"""
Configuration and constants for Investment Planner
"""

# App Configuration
APP_TITLE = "Investment Planner - SIP & SWP Calculator"
APP_ICON = "💰"
LAYOUT = "wide"

# Color Scheme - Modern Teal/Purple
COLORS = {
    'primary': '#0EA5E9',        # Sky Blue
    'primary_dark': '#0284C7',
    'secondary': '#8B5CF6',      # Purple
    'accent': '#F59E0B',         # Amber
    'success': '#10B981',        # Emerald
    'danger': '#EF4444',         # Red
    'warning': '#F59E0B',        # Amber
}

# Default Values
DEFAULTS = {
    'sip': {
        'monthly_amount': 10000,
        'annual_return': 12.0,
        'years': 20,
        'step_up': 5.0,
        'inflation': 6.0,
    },
    'swp': {
        'initial_corpus': 1000000,
        'annual_return': 8.0,
        'years': 25,
        'monthly_withdrawal': 50000,
        'step_up': 5.0,
        'inflation': 6.0,
    },
    'retirement': {
        'current_age': 35,
        'retirement_age': 60,
        'target_goal': 10000000,
        'annual_return': 12.0,
        'step_up': 10.0,
        'inflation': 6.0,
    }
}

# Slider Ranges
RANGES = {
    'monthly_sip': {'min': 500, 'max': 1000000, 'step': 500},
    'annual_return': {'min': 1.0, 'max': 30.0, 'step': 0.5},
    'years': {'min': 1, 'max': 40, 'step': 1},
    'step_up': {'min': 0.0, 'max': 20.0, 'step': 0.5},
    'inflation': {'min': 0.0, 'max': 15.0, 'step': 0.5},
    'initial_corpus': {'min': 1000000, 'max': 1000000000, 'step': 50000},
    'monthly_withdrawal': {'min': 0, 'max': 2000000, 'step': 5000},
    'swp_years': {'min': 5, 'max': 50, 'step': 1},
    'age': {'min': 18, 'max': 80, 'step': 1},
    'retirement_goal': {'min': 1000000, 'max': 500000000, 'step': 500000},
}

# Currency Options
CURRENCIES = ["$", "₹", "€"]

# Calculator Modes
CALCULATOR_MODES = [
    "SIP Calculator",
    "SWP Calculator",
    "Retirement Planner"
]

# Contribution Timing Options
CONTRIBUTION_TIMING = ["Beginning", "End"]