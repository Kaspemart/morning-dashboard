import os
import subprocess
from datetime import datetime

from dashboard import build_html
from data import fetch_data
from notify import check_alerts, send_email

DASHBOARD_URL = "https://kaspemart.github.io/morning-dashboard"


def push_dashboard(html):
    with open("index.html", "w") as f:
        f.write(html)
    subprocess.run(["git", "add", "index.html"], check=True)
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

    print("Building dashboard...")
    html = build_html(hist, info)

    print("Pushing to GitHub Pages...")
    push_dashboard(html)

    if os.environ.get("SEZNAM_USER"):
        print("Sending email...")
        send_email(DASHBOARD_URL)
    else:
        print(f"Email env vars not set — dashboard at {DASHBOARD_URL}")

    print("Done.")


if __name__ == "__main__":
    main()
