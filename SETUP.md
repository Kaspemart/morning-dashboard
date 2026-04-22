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

## 3. Create a sender email account

Create a dedicated throwaway email account used only for sending (e.g. seznam.cz works well). This account's credentials will be stored in the Claude Routine, so don't use a personal account.

## 4. Set environment variables

Add these to your `~/.zshrc` (Mac/zsh) or `~/.bashrc` (Linux/bash):

```bash
export SEZNAM_USER=your.sender@seznam.cz   # the throwaway sending account
export SEZNAM_PASS=your_password
```

Then reload:

```bash
source ~/.zshrc
```

> If using a different email provider, update the SMTP server and port in `send_email()` in `main.py`.

## 5. Update the recipient email

In `main.py`, find the `send_email` function and change the recipient:

```python
recipient = "your.name@yourcompany.com"
```

## 6. Enable GitHub Pages

In the GitHub repo: **Settings → Pages → Source → Deploy from a branch → main / root → Save**.

The dashboard will be live at `https://<your-github-username>.github.io/morning-dashboard`.

## 7. Test it

```bash
uv run python main.py
```

Check that `index.html` was pushed to the repo and that you received the email.

## 8. Create the Claude Routine

In Claude Code, ask Claude to create a remote trigger that runs `uv run python main.py` every weekday at 8am your local time. Provide:
- The repo URL
- `SEZNAM_USER` and `SEZNAM_PASS` values (stored in the trigger prompt)
- Your local timezone for correct UTC conversion

Manage existing routines at: https://claude.ai/code/scheduled

## Notes

- **DST**: Cron runs in UTC. Update the trigger when clocks change (e.g. `0 6 * * 1-5` in summer, `0 7 * * 1-5` in winter for Prague/CET).
- **Extending the dashboard**: Add new data sources and Plotly figures in `main.py` inside `build_html()`.
