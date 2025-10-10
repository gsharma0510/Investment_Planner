# calculators/sip.py
"""
SIP (Systematic Investment Plan) calculation logic
"""
import numpy as np
import pandas as pd
from .helpers import annual_to_monthly_rate, real_annual_return, sip_future_value_annuity_due


def simulate_sip(monthly_contribution, annual_return, years,
                 step_up=0.0, adjust_for_inflation=False, inflation=0.0,
                 contribution_at_beginning=True):
    """
    Simulate SIP investment with step-up and inflation adjustment

    Returns:
        df_monthly: Monthly simulation DataFrame
        df_year: Yearly summary DataFrame
        fv_nominal: Final nominal corpus
        fv_real: Inflation-adjusted corpus
        total_invested_nominal: Total nominal investment
        total_invested_real: Total real investment (today's value)
    """
    years = int(round(years))
    n_months = years * 12
    monthly_nom_r = annual_to_monthly_rate(annual_return)

    total_invested_nominal = 0.0
    total_invested_real = 0.0

    if adjust_for_inflation and inflation > 0:
        r_real = real_annual_return(annual_return, inflation)
        monthly_real_r = annual_to_monthly_rate(r_real)

        fv_nominal = 0.0
        fv_real = 0.0

        for year_idx in range(years):
            nominal_contribution = monthly_contribution * ((1 + step_up) ** year_idx)
            real_contribution = nominal_contribution / ((1 + inflation) ** year_idx)

            total_invested_nominal += nominal_contribution * 12
            total_invested_real += real_contribution * 12

            months_remaining = (years - year_idx) * 12

            fv_real_block = sip_future_value_annuity_due(real_contribution, monthly_real_r, 12)
            if months_remaining > 12:
                fv_real_block *= (1 + monthly_real_r) ** (months_remaining - 12)
            fv_real += fv_real_block

            fv_nom_block = sip_future_value_annuity_due(nominal_contribution, monthly_nom_r, 12)
            if months_remaining > 12:
                fv_nom_block *= (1 + monthly_nom_r) ** (months_remaining - 12)
            fv_nominal += fv_nom_block

    else:
        fv_nominal = 0.0
        for year_idx in range(years):
            p_year = monthly_contribution * ((1 + step_up) ** year_idx)
            total_invested_nominal += p_year * 12
            total_invested_real += p_year * 12

            months_remaining = (years - year_idx) * 12
            fv_of_year_block = sip_future_value_annuity_due(p_year, monthly_nom_r, 12)
            if months_remaining > 12:
                fv_of_year_block *= (1 + monthly_nom_r) ** (months_remaining - 12)
            fv_nominal += fv_of_year_block

        fv_real = fv_nominal

    # Monthly simulation
    balance = 0.0
    monthly_balances = []
    monthly_contribs = []
    dates = pd.date_range(start=pd.Timestamp.today().normalize(), periods=n_months, freq='M')

    for m in range(n_months):
        year_idx = m // 12
        current_monthly = monthly_contribution * ((1 + step_up) ** year_idx)

        if contribution_at_beginning:
            balance += current_monthly
            balance *= (1 + monthly_nom_r)
        else:
            balance *= (1 + monthly_nom_r)
            balance += current_monthly
        monthly_balances.append(balance)
        monthly_contribs.append(current_monthly)

    df_monthly = pd.DataFrame({
        "date": dates,
        "month_index": np.arange(1, n_months + 1),
        "monthly_contribution": monthly_contribs,
        "balance": monthly_balances
    }).set_index("date")

    # Yearly summary
    df_year = df_monthly.resample("Y").agg({
        "monthly_contribution": "sum",
        "balance": ["first", "last"]
    })
    df_year.columns = ["annual_contribution", "begin_balance", "end_balance"]
    df_year["interest_earned"] = df_year["end_balance"] - df_year["begin_balance"] + df_year["annual_contribution"]
    df_year = df_year.reset_index()
    df_year["year"] = df_year["date"].dt.year.astype(int)

    return df_monthly, df_year, fv_nominal, fv_real, total_invested_nominal, total_invested_real


def find_required_monthly_sip(target_corpus, annual_return, years,
                              step_up=0.0, adjust_for_inflation=False, inflation=0.0,
                              contribution_at_beginning=True, tol=0.01, max_iter=80):
    """
    Back-calculate required monthly SIP to reach target corpus
    Uses binary search algorithm
    """
    low, high = 0.0, 10000.0

    def fv_for_p(p):
        _, _, fv_nom, fv_real, _, _ = simulate_sip(
            p, annual_return, years, step_up, adjust_for_inflation, inflation, contribution_at_beginning
        )
        return fv_real if adjust_for_inflation else fv_nom

    # Expand range if needed
    while fv_for_p(high) < target_corpus:
        high *= 2
        if high > 1e9:
            break

    # Binary search
    for _ in range(max_iter):
        mid = (low + high) / 2.0
        fv_mid = fv_for_p(mid)
        if abs(fv_mid - target_corpus) <= tol:
            return mid
        if fv_mid < target_corpus:
            low = mid
        else:
            high = mid

    return (low + high) / 2.0