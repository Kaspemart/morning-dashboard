from datetime import datetime

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data import calculate_rsi


def build_html(hist, info):
    current_price = info.last_price
    prev_close = info.previous_close
    day_change = current_price - prev_close
    day_change_pct = (day_change / prev_close) * 100

    hist_3m = hist.iloc[-63:] if len(hist) >= 63 else hist
    high_3m = hist_3m["Close"].max()
    low_3m = hist_3m["Close"].min()

    hist_week = hist.iloc[-5:] if len(hist) >= 5 else hist
    price_week_ago = hist_week["Close"].iloc[0]
    weekly_change_pct = (current_price - price_week_ago) / price_week_ago * 100

    year_start = hist["Close"].iloc[0]
    ytd_change_pct = ((current_price - year_start) / year_start) * 100

    rsi = calculate_rsi(hist["Close"])
    rsi_color = "#22c55e" if rsi < 40 else "#ef4444" if rsi > 65 else "#e2e8f0"

    arrow_day = "▲" if day_change >= 0 else "▼"
    arrow_week = "▲" if weekly_change_pct >= 0 else "▼"

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.05,
    )

    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist["Close"],
            mode="lines",
            name="VUAG.L",
            line=dict(color="#2563eb", width=2),
            hovertemplate="%{x|%b %d, %Y}<br>£%{y:,.2f}<extra></extra>",
        ),
        row=1, col=1,
    )

    fig.add_trace(
        go.Bar(
            x=hist.index,
            y=hist["Volume"],
            name="Volume",
            marker_color="#93c5fd",
            hovertemplate="%{x|%b %d, %Y}<br>Vol: %{y:,.0f}<extra></extra>",
        ),
        row=2, col=1,
    )

    fig.update_layout(
        title=dict(text="Vanguard S&P 500 (Acc) — VUAG.L — 1 Year", font=dict(size=20)),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(color="#e2e8f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        margin=dict(l=60, r=40, t=80, b=40),
        xaxis2=dict(showgrid=False),
        yaxis=dict(gridcolor="#334155", tickformat=",.0f", tickprefix="£"),
        yaxis2=dict(gridcolor="#334155", tickformat=".2s"),
    )

    chart_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
    generated = datetime.now().strftime("%A, %B %d %Y — %H:%M")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Morning Dashboard — {datetime.now().strftime("%b %d, %Y")}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #0f172a; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; padding: 24px; }}
    h1 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 4px; }}
    .subtitle {{ color: #94a3b8; font-size: 0.875rem; margin-bottom: 24px; }}
    .stats {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }}
    .card {{ background: #1e293b; border-radius: 12px; padding: 16px 24px; flex: 1; min-width: 150px; }}
    .card-label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }}
    .card-value {{ font-size: 1.4rem; font-weight: 700; }}
    .positive {{ color: #22c55e; }}
    .negative {{ color: #ef4444; }}
    .chart-wrapper {{ background: #1e293b; border-radius: 12px; padding: 8px; }}
  </style>
</head>
<body>
  <h1>Morning Dashboard</h1>
  <p class="subtitle">Generated {generated} (Prague time)</p>

  <div class="stats">
    <div class="card">
      <div class="card-label">Vanguard S&amp;P 500</div>
      <div class="card-value">£{current_price:,.2f}</div>
    </div>
    <div class="card">
      <div class="card-label">Day Change</div>
      <div class="card-value {'positive' if day_change >= 0 else 'negative'}">{arrow_day} £{abs(day_change):,.2f} ({day_change_pct:+.2f}%)</div>
    </div>
    <div class="card">
      <div class="card-label">Week Change</div>
      <div class="card-value {'positive' if weekly_change_pct >= 0 else 'negative'}">{arrow_week} {weekly_change_pct:+.2f}%</div>
    </div>
    <div class="card">
      <div class="card-label">YTD</div>
      <div class="card-value {'positive' if ytd_change_pct >= 0 else 'negative'}">{ytd_change_pct:+.2f}%</div>
    </div>
    <div class="card">
      <div class="card-label">3M High</div>
      <div class="card-value">£{high_3m:,.2f}</div>
    </div>
    <div class="card">
      <div class="card-label">3M Low</div>
      <div class="card-value">£{low_3m:,.2f}</div>
    </div>
    <div class="card">
      <div class="card-label">RSI (14-day)</div>
      <div class="card-value" style="color: {rsi_color}">{rsi:.1f}</div>
    </div>
  </div>

  <div class="chart-wrapper">
    {chart_html}
  </div>
</body>
</html>"""
