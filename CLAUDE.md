# Morning Dashboard

A weekday morning briefing system that generates an interactive financial dashboard and emails a link to it each day at 8am Prague time (Europe/Prague).

## What it does

A Claude Code Routine runs `main.py` every weekday morning. It:
1. Fetches S&P 500 data via `yfinance`
2. Builds an interactive `index.html` dashboard using Plotly (client-side, no server needed)
3. Commits and pushes `index.html` to this repo
4. Sends an email with a link to the live dashboard

The dashboard is served via **GitHub Pages** at `https://kaspemart.github.io/morning-dashboard`.

## Stack

| Component   | Tool                                      |
|-------------|-------------------------------------------|
| Data        | yfinance (S&P 500), more APIs later       |
| Charts      | Plotly (interactive, client-side)         |
| Hosting     | GitHub Pages (static HTML, no cold start) |
| Notification| Email via Gmail + smtplib                 |
| Scheduler   | Claude Code Routine, 8am Prague time      |

## Project structure

```
main.py          # Entry point — fetch data, build HTML, send email
index.html       # Generated dashboard (committed each run, served by Pages)
pyproject.toml   # Python dependencies (uv)
```

## Environment variables required

| Variable       | Purpose                                      |
|----------------|----------------------------------------------|
| `SEZNAM_USER`  | seznam.cz address used to send               |
| `SEZNAM_PASS`  | seznam.cz password                           |

## Extending

The dashboard is designed to grow. To add a new section (e.g. macro data, portfolio tracker, news summary), add a new data-fetch function and a new Plotly figure or HTML block in `main.py`, then include it in the `build_html()` output.
