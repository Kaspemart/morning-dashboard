import subprocess
from datetime import datetime
from pathlib import Path

from dashboard import build_html
from data import fetch_data
from news import fetch_news
from notify import check_alerts, send_morning_notification

DASHBOARD_URL = "https://kaspemart.github.io/morning-dashboard"


def push_dashboard(html):
    with open("index.html", "w") as f:
        f.write(html)
    subprocess.run(["git", "add", "index.html"], check=True)
    today_history = Path(f"news_history/{datetime.now().strftime('%Y-%m-%d')}.md")
    if today_history.exists():
        subprocess.run(["git", "add", str(today_history)], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Dashboard update {datetime.now().strftime('%Y-%m-%d')}"],
        check=True,
    )
    subprocess.run(["git", "push", "origin", "main"], check=True)


def main():
    print("Fetching VUAG.L data...")
    hist, info = fetch_data()

    print("Checking alerts...")
    check_alerts(hist, info)

    print("Fetching news briefing...")
    news_md = fetch_news()

    print("Building dashboard...")
    html = build_html(hist, info, news_md)

    print("Pushing to GitHub Pages...")
    push_dashboard(html)

    print("Sending morning notification...")
    send_morning_notification()

    print("Done.")


if __name__ == "__main__":
    main()
