# 💰 Investment Planner — SIP & SWP Calculator

A professional, modular investment planning tool built with Python and Streamlit.
Covers SIP (Systematic Investment Plan), SWP (Systematic Withdrawal Plan), and Retirement Goal back-calculation — with inflation adjustment, step-up logic, and interactive charts.

---

## 🚀 Quick Start

```bash
# 1. Clone or download the project
cd investment_planner

# 2. Create and activate a virtual environment
python -m venv inv_plan_venv
inv_plan_venv\Scripts\activate        # Windows
source inv_plan_venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## ✨ Features

| Feature | Status |
|---|---|
| SIP Calculator with step-up | ✅ |
| SWP Calculator with step-up | ✅ |
| Retirement Goal back-calculator | ✅ |
| Inflation adjustment (Fisher's real rate) | ✅ |
| Nominal vs Real corpus display | ✅ |
| Interactive Plotly charts | ✅ |
| Year-by-year breakdown table | ✅ |
| Currency selector (USD / INR / EUR / GBP) | ✅ |
| Contribution timing (Beginning / End of month) | ✅ |
| Monte Carlo Simulation | 🔜 Next |
| AI Advisor (LLM API) | 🔜 Planned |
| PDF report export | 🔜 Planned |

---

## 🧮 Calculation Methodology

All core formulas are implemented in `calculators/`. No logic lives in UI files.

### SIP — Future Value (Annuity Due)
```
FV = P × ((1+r)ⁿ - 1) / r × (1+r)

where:
  P = monthly contribution
  r = monthly rate = (1 + annual_rate)^(1/12) - 1
  n = total months
```

### Step-Up Logic
```
P_year = P_0 × (1 + step_up_rate)^(year - 1)
```

### Inflation Adjustment — Fisher's Real Rate
```
r_real = (1 + r_nominal) / (1 + inflation) - 1

Real contribution = Nominal contribution / (1 + inflation)^year
```
When inflation adjustment is on, the binary-search back-calculator targets
the **real** corpus (today's purchasing power), not the nominal number.
The table always shows nominal figures — a callout explains the difference.

### SWP — Closed-Form Annual Reconciliation
```
End = Begin × (1+i)^12 - W × ((1+i)^12 - 1) / i

where:
  i = monthly return rate
  W = monthly withdrawal
```
The monthly simulation loop and the yearly closed-form use slightly different
compounding boundaries by design — comments in `swp.py` explain both.

### Retirement Back-Calculator
Uses binary search (80 iterations, tolerance ₹0.01) over `simulate_sip()`
to find the starting monthly SIP that produces the target corpus.

---

## 📁 Project Structure

```
investment_planner/
│
├── app.py                          # Main entry point — page config, sidebar, routing
├── config.py                       # All constants: defaults, ranges, SS keys, currencies
├── requirements.txt
│
├── styles/
│   ├── __init__.py
│   └── custom_css.py               # All CSS in one place (Inter font, metric cards, sidebar)
│
├── calculators/                    # Pure calculation logic — no Streamlit imports
│   ├── __init__.py
│   ├── helpers.py                  # annual_to_monthly_rate, Fisher formula, format_currency_str
│   ├── sip.py                      # simulate_sip(), find_required_monthly_sip()
│   └── swp.py                      # simulate_swp(), max_sustainable_withdrawal()
│
├── components/                     # Reusable UI building blocks
│   ├── __init__.py
│   ├── metrics.py                  # metric_card() — used across all three pages
│   ├── charts.py                   # create_line_chart(), create_swp_chart(), create_retirement_chart()
│   └── hero.py                     # Hero banner HTML
│
└── views/                          # One file per calculator page
    ├── __init__.py
    ├── sip_calculator.py           # render_sip_calculator(currency)
    ├── swp_calculator.py           # render_swp_calculator(currency)
    └── retirement_planner.py       # render_retirement_planner(currency)
```

### Why This Structure?

**Separation of concerns** — calculators know nothing about Streamlit. You can
unit-test `sip.py` with plain Python, no UI required.

**Token efficiency** — when resuming development with an AI assistant, share
only the file(s) relevant to the current task rather than the entire codebase.
Editing `views/sip_calculator.py` (150 lines) costs ~500 tokens vs ~3,000 for
a 600-line monolith.

**Single source of truth** — all defaults, slider ranges, and session-state
key names live in `config.py`. Change a default once, it propagates everywhere.

---

## ⚙️ Key Design Decisions

### Session State Namespacing
All Streamlit session-state keys are defined in `config.SS` with page prefixes
(`sip__`, `swp__`, `ret__`). This prevents slider values from one calculator
bleeding into another when the user switches modes.

```python
# config.py
SS = {
    "sip_amount":        "sip__monthly_amount",
    "sip_amount_slider": "sip__monthly_amount_slider",
    ...
}
```

### Currency Encoding
Symbols are stored as Unicode escape sequences in `config.py` to avoid
file-encoding issues across Windows / macOS / Linux:
- ₹ → `\u20b9`
- € → `\u20ac`
- £ → `\u00a3`

### Yearly Table — Simulation Year Boundaries
The yearly breakdown table groups by **simulation year** (every 12 months
from start date) rather than calendar year. This avoids a partial final row
that appears when `resample("Y")` cuts at December 31st mid-simulation.

---

## 📦 Requirements

```
streamlit>=1.28
plotly>=5.17
pandas
numpy
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🗺️ Development Roadmap

| Phase | Description | Status |
|---|---|---|
| **Phase 0** | Core calculations (SIP, SWP, Retirement) | ✅ Complete |
| **Phase 1** | Modular architecture, UI polish, bug fixes | ✅ Complete |
| **Phase 2** | Monte Carlo simulation engine | 🔜 Next |
| **Phase 3** | AI Advisor (Claude API integration) | 🔜 Planned |
| **Phase 4** | Goal wizard, Scenario comparison | 🔜 Planned |
| **Phase 5** | PDF reports, Excel export, Shareable links | 🔜 Planned |

---
