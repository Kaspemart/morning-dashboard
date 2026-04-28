# Morning Dashboard

A personal financial dashboard that runs every weekday morning, updates a GitHub Pages site with interactive charts, and sends a push notification to the owner's phone.

## What it does

A **GitHub Actions workflow** runs `main.py` every weekday at 8am Prague time. It:
1. Fetches full historical data for **Vanguard S&P 500 UCITS ETF (VUAG.L)** via `yfinance`
2. Checks two buy alert conditions and sends push notifications if triggered
3. Builds an interactive `index.html` dashboard using Plotly
4. Commits and pushes `index.html` to this repo (served via GitHub Pages)
5. Sends a daily "Your morning dashboard is ready" push notification with a tap-to-open link

Dashboard URL: **https://kaspemart.github.io/morning-dashboard**

## Stack

| Component    | Tool                                                  |
|--------------|-------------------------------------------------------|
| Data         | yfinance — VUAG.L, full history (`period="max"`)      |
| Charts       | Plotly — interactive, client-side, time range buttons |
| Hosting      | GitHub Pages — static HTML, no server needed          |
| Notifications| ntfy.sh — push notifications, no credentials needed   |
| Scheduler    | GitHub Actions — weekdays at 8am Prague time          |

## Project structure

```
main.py                              # Orchestrates everything
data.py                              # Fetches VUAG.L data
dashboard.py                         # Builds the HTML dashboard
notify.py                            # ntfy alerts + morning notification
index.html                           # Generated dashboard (auto-committed daily)
.github/workflows/morning-dashboard.yml  # GitHub Actions schedule
pyproject.toml                       # Python dependencies (managed with uv)
SETUP.md                             # Onboarding guide for new users
```

## Notifications (ntfy.sh)

All notifications go to topic: `morning-snp-notification`

To receive notifications: install the **ntfy app** (iOS/Android) and subscribe to `morning-snp-notification`. No account needed.

Three notification types:
- **Daily morning**: "Your morning dashboard is ready." — tapping opens the dashboard
- **Buy alert**: when VUAG.L drops 7%+ from its 3-month high — "Good opportunity to buy more S&P 500"
- **Weekly drop alert**: when VUAG.L drops 3%+ in the last 7 days — "Consider topping up your S&P 500 investment"

## Dashboard stat cards

| Card              | Description                              |
|-------------------|------------------------------------------|
| Vanguard S&P 500  | Current VUAG.L price in GBP              |
| Day Change        | £ and % change from previous close       |
| Week Change       | % change over last 5 trading days        |
| YTD               | % change since start of year             |
| 3M High           | Highest price in last 3 months           |
| 3M Low            | Lowest price in last 3 months            |

## Chart

Interactive Plotly line chart with area fill. Time range buttons: **1D / 1W / 1M / 3M / 1Y / 5Y / Max**. Fetches full history so all buttons work.

## Scheduler

GitHub Actions workflow: `.github/workflows/morning-dashboard.yml`

- Cron: `0 5 * * 1-5` (7am Prague, CEST/UTC+2 — **change to `0 6 * * 1-5` in winter when clocks go back to CET/UTC+1**)
- Can also be triggered manually: GitHub repo → Actions → Morning Dashboard → Run workflow
- Uses `GITHUB_TOKEN` for git push — no secrets needed

## No environment variables required

Everything runs without credentials. ntfy.sh is credential-free. Git push uses the built-in `GITHUB_TOKEN` in GitHub Actions.

## Extending

- **New data**: add fetch functions in `data.py`
- **New chart/section**: add to `build_html()` in `dashboard.py`
- **New alert**: add to `check_alerts()` in `notify.py`
- **New ntfy topic**: update `NTFY_TOPIC` in `notify.py`

## Running locally

```bash
uv sync
uv run python main.py
```

Note: running locally will commit and push `index.html` to the repo. Make sure you're on the `main` branch with a clean working tree.
