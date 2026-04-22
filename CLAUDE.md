# Morning Dashboard

A weekday morning briefing system that generates an interactive financial dashboard and sends a push notification each day at 8am Prague time (Europe/Prague).

## What it does

A Claude Code Routine runs `main.py` every weekday morning. It:
1. Fetches Vanguard S&P 500 (VUAG.L) data via `yfinance`
2. Checks buy alerts (7% drop from 3-month high, 3% weekly drop)
3. Builds an interactive `index.html` dashboard using Plotly (client-side, no server needed)
4. Commits and pushes `index.html` to this repo
5. Sends a push notification via ntfy with a link to the dashboard

The dashboard is served via **GitHub Pages** at `https://kaspemart.github.io/morning-dashboard`.

## Stack

| Component    | Tool                                      |
|--------------|-------------------------------------------|
| Data         | yfinance (VUAG.L)                         |
| Charts       | Plotly (interactive, client-side)         |
| Hosting      | GitHub Pages (static HTML, no cold start) |
| Notification | ntfy.sh push notifications                |
| Scheduler    | Claude Code Routine, 8am Prague time      |

## Project structure

```
main.py        # Entry point — orchestrates everything
data.py        # Data fetching and RSI calculation
dashboard.py   # HTML/chart building
notify.py      # ntfy alerts and morning notification
index.html     # Generated dashboard (committed each run, served by Pages)
pyproject.toml # Python dependencies (uv)
```

## No environment variables required

Notifications are sent via ntfy.sh — no credentials needed.

## Alerts

- **Buy alert**: notifies when VUAG.L drops 7%+ from its 3-month high
- **Weekly drop alert**: notifies when VUAG.L drops 3%+ in the last 7 days
- **Morning notification**: daily "Your morning dashboard is ready" with a tap-to-open link

All notifications go to ntfy topic `morning-snp-notification`.

## Extending

To add a new section (e.g. macro data, portfolio tracker, news summary), add a new data-fetch function in `data.py` and a new Plotly figure or HTML block in `dashboard.py`.
