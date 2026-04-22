import os
import smtplib
import subprocess
from datetime import datetime
from email.mime.text import MIMEText

import plotly.graph_objects as go
import yfinance as yf
from plotly.subplots import make_subplots


def fetch_sp500():
    ticker = yf.Ticker("^GSPC")
    hist = ticker.history(period="1y")
    info = ticker.fast_info
    return hist, info


def build_html(hist, info):
    current_price = info.last_price
    prev_close = info.previous_close
    day_change = current_price - prev_close
    day_change_pct = (day_change / prev_close) * 100
    year_start = hist["Close"].iloc[0]
    ytd_change_pct = ((current_price - year_start) / year_start) * 100
    high_52w = hist["Close"].max()
    low_52w = hist["Close"].min()

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
            name="S&P 500",
            line=dict(color="#2563eb", width=2),
            hovertemplate="%{x|%b %d, %Y}<br>%{y:,.2f}<extra></extra>",
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
        title=dict(text="S&P 500 — 1 Year", font=dict(size=20)),
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(color="#e2e8f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        margin=dict(l=60, r=40, t=80, b=40),
        xaxis2=dict(showgrid=False),
        yaxis=dict(gridcolor="#334155", tickformat=",.0f"),
        yaxis2=dict(gridcolor="#334155", tickformat=".2s"),
    )

    chart_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

    change_color = "#22c55e" if day_change >= 0 else "#ef4444"
    ytd_color = "#22c55e" if ytd_change_pct >= 0 else "#ef4444"
    arrow = "▲" if day_change >= 0 else "▼"

    generated = datetime.now().strftime("%A, %B %d %Y — %H:%M")

    html = f"""<!DOCTYPE html>
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
    .card {{ background: #1e293b; border-radius: 12px; padding: 16px 24px; flex: 1; min-width: 160px; }}
    .card-label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }}
    .card-value {{ font-size: 1.5rem; font-weight: 700; }}
    .card-value.positive {{ color: #22c55e; }}
    .card-value.negative {{ color: #ef4444; }}
    .chart-wrapper {{ background: #1e293b; border-radius: 12px; padding: 8px; }}
  </style>
</head>
<body>
  <h1>Morning Dashboard</h1>
  <p class="subtitle">Generated {generated} (Prague time)</p>

  <div class="stats">
    <div class="card">
      <div class="card-label">S&amp;P 500</div>
      <div class="card-value">{current_price:,.2f}</div>
    </div>
    <div class="card">
      <div class="card-label">Day Change</div>
      <div class="card-value {'positive' if day_change >= 0 else 'negative'}">{arrow} {abs(day_change):,.2f} ({day_change_pct:+.2f}%)</div>
    </div>
    <div class="card">
      <div class="card-label">YTD</div>
      <div class="card-value {'positive' if ytd_change_pct >= 0 else 'negative'}">{ytd_change_pct:+.2f}%</div>
    </div>
    <div class="card">
      <div class="card-label">52W High</div>
      <div class="card-value">{high_52w:,.2f}</div>
    </div>
    <div class="card">
      <div class="card-label">52W Low</div>
      <div class="card-value">{low_52w:,.2f}</div>
    </div>
  </div>

  <div class="chart-wrapper">
    {chart_html}
  </div>
</body>
</html>"""

    return html


def push_dashboard(html):
    with open("index.html", "w") as f:
        f.write(html)
    subprocess.run(["git", "add", "index.html"], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Dashboard update {datetime.now().strftime('%Y-%m-%d')}"],
        check=True,
    )
    subprocess.run(["git", "push", "origin", "main"], check=True)


def send_email(dashboard_url):
    seznam_user = os.environ["SEZNAM_USER"]
    seznam_pass = os.environ["SEZNAM_PASS"]
    recipient = "martin.kasperlik@rsj.com"

    body = f"Your morning dashboard is ready:\n\n{dashboard_url}\n"
    msg = MIMEText(body)
    msg["Subject"] = f"Morning Dashboard — {datetime.now().strftime('%b %d, %Y')}"
    msg["From"] = seznam_user
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.seznam.cz", 465) as server:
        server.login(seznam_user, seznam_pass)
        server.sendmail(seznam_user, recipient, msg.as_string())


def main():
    print("Fetching S&P 500 data...")
    hist, info = fetch_sp500()

    print("Building dashboard...")
    html = build_html(hist, info)

    print("Pushing to GitHub Pages...")
    push_dashboard(html)

    dashboard_url = "https://kaspemart.github.io/morning-dashboard"

    if os.environ.get("SEZNAM_USER"):
        print("Sending email...")
        send_email(dashboard_url)
    else:
        print(f"Email env vars not set — dashboard at {dashboard_url}")

    print("Done.")


if __name__ == "__main__":
    main()
