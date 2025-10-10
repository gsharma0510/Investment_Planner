# calculators/helpers.py
"""
Utility functions for financial calculations
"""
import numpy as np

def annual_to_monthly_rate(annual_rate):
    """Convert annual rate to monthly rate"""
    return (1 + annual_rate) ** (1/12) - 1

def real_annual_return(nominal, inflation):
    """Calculate real return using Fisher's formula"""
    return (1 + nominal) / (1 + inflation) - 1

def format_currency_str(symbol, val):
    """Format currency with symbol and commas"""
    return f"{symbol}{int(round(val)):,}"

def sip_future_value_annuity_due(monthly_p, monthly_r, n_months):
    """
    Calculate future value of annuity due (beginning of period)
    FV = P * ((1+r)^n - 1)/r * (1+r)
    """
    if abs(monthly_r) < 1e-12:
        return monthly_p * n_months
    return monthly_p * ((1 + monthly_r) ** n_months - 1) / monthly_r * (1 + monthly_r)