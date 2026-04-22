# Setup Guide

Steps to get the morning dashboard running from scratch on a new machine.

## 1. Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- Git configured with access to your GitHub account

## 2. Clone the repo and install dependencies

```bash
git clone https://github.com/Kaspemart/morning-dashboard
cd morning-dashboard
uv sync
```

## 3. Fix SSL certificates (Mac only)

Python on Mac requires a one-time certificate install to make HTTPS requests:

```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

## 4. Set up ntfy on your phone

1. Install the **ntfy** app (free, iOS/Android)
2. Subscribe to topic: `morning-snp-notification`

That's it — no account or credentials needed.

## 5. Enable GitHub Pages

In the GitHub repo: **Settings → Pages → Source → Deploy from a branch → main / root → Save**.

The dashboard will be live at `https://<your-github-username>.github.io/morning-dashboard`.

Update `DASHBOARD_URL` in `notify.py` to match your GitHub Pages URL.

## 6. Test it

```bash
uv run python main.py
```

Check that `index.html` was pushed to the repo and that you received a push notification on your phone.

## 7. Create the Claude Routine

In Claude Code, ask Claude to create a remote trigger that runs `uv run python main.py` every weekday at 8am your local time. Provide the repo URL and your local timezone for correct UTC conversion.

Manage existing routines at: https://claude.ai/code/scheduled

## Notes

- **DST**: Cron runs in UTC. Update the trigger when clocks change (e.g. `0 6 * * 1-5` in summer CEST, `0 7 * * 1-5` in winter CET for Prague).
- **Alert thresholds**: configured in `notify.py` — 7% drop from 3-month high, 3% weekly drop.
- **Extending the dashboard**: add new data sources and Plotly figures in `data.py` and `dashboard.py`.
