# components/metrics.py
"""
Metric card components for displaying financial data
"""


def metric_card(label, value, delta=None, delta_type="neutral"):
    """
    Create a beautiful metric card with optional delta

    Args:
        label: Metric label (e.g., "Total Invested")
        value: Main value to display
        delta: Optional delta text (e.g., "+50%")
        delta_type: Type of delta - "positive", "negative", or "neutral"

    Returns:
        HTML string for metric card
    """
    delta_class = f"metric-delta-{delta_type}"
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ''

    html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    return html