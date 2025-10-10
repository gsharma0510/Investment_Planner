# calculators/swp.py
"""
SWP (Systematic Withdrawal Plan) calculation logic
"""
import numpy as np
import pandas as pd
from .helpers import annual_to_monthly_rate


def simulate_swp(initial_corpus, annual_return, years, monthly_withdrawal,
                 step_up=0.0, adjust_for_inflation=False, inflation=0.0):
    """
    Simulate SWP with step-up withdrawals

    Returns:
        df_monthly: Monthly simulation DataFrame
        df_year: Yearly summary DataFrame
        exhausted_month: Month when corpus is exhausted (or None)
    """
    years = int(round(years))
    monthly_r = annual_to_monthly_rate(annual_return)
    n_months = years * 12
    dates = pd.date_range(start=pd.Timestamp.today().normalize(), periods=n_months, freq='M')

    # Monthly simulation
    balances = []
    withdrawals = []
    balance = float(initial_corpus)
    current_withdrawal = float(monthly_withdrawal)
    exhausted_month = None

    for m in range(n_months):
        balance = balance * (1 + monthly_r)
        balance -= current_withdrawal
        balances.append(balance)
        withdrawals.append(current_withdrawal)

        if balance < 0 and exhausted_month is None:
            exhausted_month = dates[m]

        # Apply step-up at year end
        if (m + 1) % 12 == 0:
            current_withdrawal *= (1 + step_up)

    df_monthly = pd.DataFrame({
        "date": dates,
        "month_index": np.arange(1, n_months + 1),
        "monthly_withdrawal": withdrawals,
        "balance": balances
    }).set_index("date")

    # Yearly reconciliation using closed-form
    records = []
    begin_balance = float(initial_corpus)
    current_monthly_w = float(monthly_withdrawal)

    for y in range(1, years + 1):
        if abs(monthly_r) < 1e-12:
            # Zero rate edge case
            annual_withdrawal = current_monthly_w * 12
            end_balance = begin_balance - annual_withdrawal
            interest_earned = 0.0
        else:
            annual_withdrawal = current_monthly_w * 12
            annuity_factor = ((1 + monthly_r) ** 12 - 1) / monthly_r
            end_balance = begin_balance * (1 + monthly_r) ** 12 - current_monthly_w * annuity_factor
            interest_earned = end_balance - begin_balance + annual_withdrawal

        records.append({
            "year": (pd.Timestamp.today().year + y - 1),
            "begin_balance": begin_balance,
            "annual_withdrawal": annual_withdrawal,
            "interest_earned": interest_earned,
            "end_balance": end_balance
        })

        begin_balance = end_balance
        current_monthly_w *= (1 + step_up)

    df_year = pd.DataFrame(records)
    return df_monthly, df_year, exhausted_month


def max_sustainable_withdrawal(initial_corpus, annual_return, years):
    """
    Calculate maximum sustainable monthly withdrawal
    Uses binary search to find withdrawal that leaves ~0 balance
    """
    low, high = 0.0, initial_corpus
    tol = 1.0
    n_months = int(round(years * 12))
    monthly_r = annual_to_monthly_rate(annual_return)

    def simulate_balance(monthly_w):
        bal = initial_corpus
        for _ in range(n_months):
            bal *= (1 + monthly_r)
            bal -= monthly_w
        return bal

    # Binary search
    for _ in range(60):
        mid = (low + high) / 2.0
        bal = simulate_balance(mid)
        if abs(bal) <= tol:
            return mid
        if bal > 0:
            low = mid
        else:
            high = mid

    return (low + high) / 2.0