# components/charts.py
"""
Chart creation functions using Plotly
"""
import plotly.graph_objects as go


def create_line_chart(df_monthly, currency, inflation=0.0, show_real=False):
    """
    Create line chart showing corpus growth over time

    Args:
        df_monthly: DataFrame with monthly data
        currency: Currency symbol
        inflation: Inflation rate (for real value calculation)
        show_real: Whether to show inflation-adjusted line

    Returns:
        Plotly figure object
    """
    fig = go.Figure()

    # Nominal corpus line
    fig.add_trace(go.Scatter(
        x=df_monthly.index,
        y=df_monthly["balance"],
        mode="lines",
        name="Nominal Corpus",
        line=dict(color='#0EA5E9', width=3),
        fill='tozeroy',
        fillcolor='rgba(14, 165, 233, 0.1)',
        hovertemplate=f"{currency}%{{y:,.0f}} on %{{x|%b %Y}}<extra></extra>"
    ))

    # Real corpus line (if enabled)
    if show_real:
        df_plot = df_monthly.copy()
        df_plot["real_balance"] = df_plot["balance"] / ((1 + inflation) ** (df_plot["month_index"] / 12.0))
        fig.add_trace(go.Scatter(
            x=df_plot.index,
            y=df_plot["real_balance"],
            mode="lines",
            name="Real Corpus (Today's Value)",
            line=dict(color='#8B5CF6', width=3, dash='dot'),
            hovertemplate=f"{currency}%{{y:,.0f}} on %{{x|%b %Y}}<extra></extra>"
        ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Corpus Value",
        hovermode='x unified',
        font=dict(family="Inter, sans-serif", size=12),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_yaxes(tickprefix=currency, tickformat=",.0f", gridcolor='rgba(0,0,0,0.05)')
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)')

    return fig


def create_swp_chart(df_monthly_no_step, df_monthly_step, currency):
    """
    Create comparison chart for SWP with and without step-up

    Args:
        df_monthly_no_step: DataFrame without step-up
        df_monthly_step: DataFrame with step-up
        currency: Currency symbol

    Returns:
        Plotly figure object
    """
    fig = go.Figure()

    # No step-up line
    fig.add_trace(go.Scatter(
        x=df_monthly_no_step.index,
        y=df_monthly_no_step["balance"],
        mode="lines",
        name="No Step-Up",
        line=dict(color='#94A3B8', width=2),
        hovertemplate=f"{currency}%{{y:,.0f}} on %{{x|%b %Y}}<extra></extra>"
    ))

    # With step-up line
    fig.add_trace(go.Scatter(
        x=df_monthly_step.index,
        y=df_monthly_step["balance"],
        mode="lines",
        name="With Step-Up",
        line=dict(color='#0EA5E9', width=3),
        fill='tozeroy',
        fillcolor='rgba(14, 165, 233, 0.1)',
        hovertemplate=f"{currency}%{{y:,.0f}} on %{{x|%b %Y}}<extra></extra>"
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Corpus Balance",
        hovermode='x unified',
        font=dict(family="Inter, sans-serif", size=12),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_yaxes(tickprefix=currency, tickformat=",.0f", gridcolor='rgba(0,0,0,0.05)')
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)')

    return fig


def create_retirement_chart(df_monthly, target_goal, currency):
    """
    Create chart for retirement goal with goal line

    Args:
        df_monthly: DataFrame with monthly data
        target_goal: Target retirement corpus
        currency: Currency symbol

    Returns:
        Plotly figure object
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_monthly.index,
        y=df_monthly["balance"],
        mode="lines",
        name="Corpus Growth",
        line=dict(color='#10B981', width=3),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.1)',
        hovertemplate=f"{currency}%{{y:,.0f}} on %{{x|%b %Y}}<extra></extra>"
    ))

    # Add goal line
    fig.add_hline(
        y=target_goal,
        line_dash="dash",
        line_color="#F59E0B",
        annotation_text=f"Goal: {currency}{int(target_goal):,}",
        annotation_position="right"
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Future Corpus Value",
        font=dict(family="Inter, sans-serif", size=12),
        height=500
    )
    fig.update_yaxes(tickprefix=currency, tickformat=",.0f", gridcolor='rgba(0,0,0,0.05)')
    fig.update_xaxes(gridcolor='rgba(0,0,0,0.05)')

    return fig