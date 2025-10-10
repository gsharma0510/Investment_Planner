# styles/custom_css.py
"""
Custom CSS styling for Investment Planner - MINIMAL FIX VERSION
Only fixes tooltip, keeps everything else working
"""


def get_custom_css():
    """Return custom CSS for the app"""
    return """
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global Styles */
        * {
            font-family: 'Inter', sans-serif;
        }

        /* Color Variables */
        :root {
            --primary-color: #0EA5E9;
            --primary-dark: #0284C7;
            --secondary-color: #8B5CF6;
            --accent-color: #F59E0B;
            --success-color: #10B981;
            --danger-color: #EF4444;
            --bg-primary: #FFFFFF;
            --bg-secondary: #F8FAFC;
            --bg-tertiary: #F1F5F9;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --border-color: #E2E8F0;
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Keep header visible and styled */
        header[data-testid="stHeader"] {
            visibility: visible !important;
            background: linear-gradient(90deg, var(--accent-color), var(--secondary-color)) !important;
            border-bottom: none !important;
            padding: 0.5rem 1rem !important;
        }

        /* Sidebar toggle button */
        button[kind="header"] {
            background-color: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 0.75rem !important;
            transition: all 0.3s ease !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
        }

        button[kind="header"]:hover {
            background-color: rgba(255, 255, 255, 0.3) !important;
            transform: scale(1.05) !important;
            border-color: rgba(255, 255, 255, 0.5) !important;
        }

        /* Main Container */
        .main {
            background-color: var(--bg-secondary);
            padding: 5rem 1rem 2rem 1rem !important;
        }

        .block-container {
            max-width: 1400px;
            padding: 2rem 3rem;
            padding-top: 5rem !important;
        }

        /* Headers */
        h1 {
            color: var(--text-primary);
            font-weight: 800;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        h2 {
            color: var(--text-primary);
            font-weight: 700;
            font-size: 1.75rem;
            margin-top: 2.5rem;
            margin-bottom: 1.5rem;
        }

        h3, h4 {
            color: var(--text-primary);
            font-weight: 600;
        }

        /* Metric Card */
        .metric-card {
            background: var(--bg-primary);
            border-radius: 16px;
            padding: 1.75rem;
            box-shadow: var(--shadow-md);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid var(--border-color);
            height: 100%;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }

        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: var(--shadow-xl);
            border-color: var(--primary-color);
        }

        .metric-card:hover::before {
            transform: scaleX(1);
        }

        .metric-label {
            color: var(--text-secondary);
            font-size: 0.813rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.75rem;
        }

        .metric-value {
            color: var(--text-primary);
            font-size: 2.25rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.75rem;
        }

        .metric-delta-positive {
            color: var(--success-color);
            font-size: 0.875rem;
            font-weight: 600;
        }

        .metric-delta-positive::before {
            content: '↗';
            font-size: 1.25rem;
            margin-right: 0.25rem;
        }

        .metric-delta-neutral {
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            border-radius: 12px;
            padding: 0.875rem 2rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(14, 165, 233, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(14, 165, 233, 0.4);
        }

        /* TOOLTIP FIX - Simple approach that doesn't break slider */
        .stSlider [data-baseweb="popover"] {
            display: none !important;
        }

        /* Number Input - Hide +/- buttons */
        .stNumberInput button {
            display: none !important;
        }

        .stNumberInput > div > div > input {
            border-radius: 12px;
            border: 2px solid var(--border-color);
            padding: 0.875rem 1rem;
            transition: all 0.3s ease;
            text-align: center;
            font-weight: 600;
        }

        .stNumberInput > div > div > input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1);
            outline: none;
        }

        /* Selectbox */
        .stSelectbox > div > div {
            border-radius: 12px;
            border: 2px solid var(--border-color);
            transition: all 0.3s ease;
        }

        .stSelectbox > div > div:focus-within {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1);
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--accent-color) 0%, var(--secondary-color) 100%);
            padding: 2rem 1.5rem;
            box-shadow: var(--shadow-lg);
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p {
            color: white !important;
            font-weight: 600;
        }

        [data-testid="stSidebar"] .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
        }

        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 3.5rem 2.5rem;
            border-radius: 24px;
            margin-bottom: 3rem;
            margin-top: 0.5rem;
            box-shadow: var(--shadow-xl);
            position: relative;
            overflow: hidden;
        }

        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
            position: relative;
            z-index: 1;
        }

        .hero-subtitle {
            font-size: 1.25rem;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }

        /* DataFrames & Charts */
        .dataframe {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow-md);
        }

        .js-plotly-plot {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: var(--shadow-md);
        }

        /* Alert boxes */
        .stAlert {
            border-radius: 12px;
            border: none;
            padding: 1rem 1.25rem;
        }
    </style>
    """