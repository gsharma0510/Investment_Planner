# config.py
"""
Configuration and constants for Investment Planner
"""

# App Configuration
APP_TITLE = "Investment Planner - SIP & SWP Calculator"
APP_ICON = "\U0001f4b0"   # 💰  — literal Unicode, no encoding ambiguity
LAYOUT = "wide"

# Color Scheme - Modern Teal/Purple
COLORS = {
    'primary':      '#0EA5E9',   # Sky Blue
    'primary_dark': '#0284C7',
    'secondary':    '#8B5CF6',   # Purple
    'accent':       '#F59E0B',   # Amber
    'success':      '#10B981',   # Emerald
    'danger':       '#EF4444',   # Red
    'warning':      '#F59E0B',   # Amber
}

# Default Values
DEFAULTS = {
    'sip': {
        'monthly_amount': 10000,
        'annual_return':  12.0,
        'years':          20,
        'step_up':        5.0,
        'inflation':      6.0,
    },
    'swp': {
        'initial_corpus':    1_000_000,
        'annual_return':     8.0,
        'years':             25,
        'monthly_withdrawal': 50_000,
        'step_up':           5.0,
        'inflation':         6.0,
    },
    'retirement': {
        'current_age':    35,
        'retirement_age': 60,
        'target_goal':    10_000_000,
        'annual_return':  12.0,
        'step_up':        10.0,
        'inflation':      6.0,
    },
}

# Slider Ranges
RANGES = {
    'monthly_sip':        {'min': 500,       'max': 1_000_000,   'step': 500},
    'annual_return':      {'min': 1.0,       'max': 30.0,        'step': 0.5},
    'years':              {'min': 1,         'max': 40,          'step': 1},
    'step_up':            {'min': 0.0,       'max': 20.0,        'step': 0.5},
    'inflation':          {'min': 0.0,       'max': 15.0,        'step': 0.5},
    'initial_corpus':     {'min': 1_000_000, 'max': 1_000_000_000, 'step': 50_000},
    'monthly_withdrawal': {'min': 0,         'max': 2_000_000,   'step': 5_000},
    'swp_years':          {'min': 5,         'max': 50,          'step': 1},
    'age':                {'min': 18,        'max': 80,          'step': 1},
    'retirement_goal':    {'min': 1_000_000, 'max': 500_000_000, 'step': 500_000},
}

# Currency Options — plain symbol strings, safe to pass directly to Plotly/format functions
CURRENCIES = [
    "$",            # US Dollar
    "\u20b9",       # ₹ Indian Rupee
    "\u20ac",       # € Euro
    "\u00a3",       # £ British Pound
]

# Calculator Modes
CALCULATOR_MODES = [
    "SIP Calculator",
    "SWP Calculator",
    "Retirement Planner",
]

# Contribution Timing Options
CONTRIBUTION_TIMING = ["Beginning", "End"]

# ── Session-state key namespacing ─────────────────────────────────────────────
# Each page prefixes its keys so switching modes never corrupts another page's
# slider state.  Import these constants instead of writing bare string literals.

SS = {
    # SIP calculator
    "sip_amount":        "sip__monthly_amount",
    "sip_amount_slider": "sip__monthly_amount_slider",
    "sip_amount_input":  "sip__monthly_amount_input",

    # SWP calculator
    "swp_corpus":           "swp__initial_corpus",
    "swp_corpus_slider":    "swp__initial_corpus_slider",
    "swp_corpus_input":     "swp__initial_corpus_input",
    "swp_withdrawal":       "swp__monthly_withdrawal",
    "swp_withdrawal_slider":"swp__monthly_withdrawal_slider",
    "swp_withdrawal_input": "swp__monthly_withdrawal_input",

    # Retirement planner
    "ret_goal":         "ret__target_goal",
    "ret_goal_slider":  "ret__target_goal_slider",
    "ret_goal_input":   "ret__target_goal_input",
}