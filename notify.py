import os
import smtplib
import urllib.request
from email.mime.text import MIMEText

NTFY_TOPIC = "morning-snp-notification"


DASHBOARD_URL = "https://kaspemart.github.io/morning-dashboard"


def send_ntfy(message, title, click_url=None):
    headers = {"Title": title}
    if click_url:
        headers["Click"] = click_url
    req = urllib.request.Request(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers=headers,
        method="POST",
    )
    urllib.request.urlopen(req)


def send_morning_notification():
    send_ntfy(
        "Your morning dashboard is ready.",
        title="Morning Dashboard",
        click_url=DASHBOARD_URL,
    )
    print("Morning notification sent")


def check_alerts(hist, info):
    current_price = info.last_price

    # Alert 1: down 7%+ from 3-month high
    hist_3m = hist.iloc[-63:] if len(hist) >= 63 else hist
    high_3m = hist_3m["Close"].max()
    drop_from_high = (current_price - high_3m) / high_3m * 100

    if drop_from_high <= -7:
        send_ntfy(
            f"VUAG.L is down {abs(drop_from_high):.1f}% from its 3-month high "
            f"(£{high_3m:,.2f} → £{current_price:,.2f}). "
            f"Good opportunity to buy more S&P 500.",
            title="S&P 500 Buy Opportunity",
            click_url=DASHBOARD_URL,
        )
        print(f"Alert sent: down {abs(drop_from_high):.1f}% from 3-month high")
    else:
        print(f"No 3-month alert: {drop_from_high:.1f}% from high")

    # Alert 2: down 3%+ over last week (~5 trading days)
    hist_week = hist.iloc[-5:] if len(hist) >= 5 else hist
    price_week_ago = hist_week["Close"].iloc[0]
    weekly_change = (current_price - price_week_ago) / price_week_ago * 100

    if weekly_change <= -3:
        send_ntfy(
            f"VUAG.L is down {abs(weekly_change):.1f}% this week "
            f"(£{price_week_ago:,.2f} → £{current_price:,.2f}). "
            f"Consider topping up your S&P 500 investment.",
            title="S&P 500 Weekly Drop Alert",
            click_url=DASHBOARD_URL,
        )
        print(f"Alert sent: down {abs(weekly_change):.1f}% this week")
    else:
        print(f"No weekly alert: {weekly_change:.1f}% this week")


def send_email(dashboard_url):
    seznam_user = os.environ["SEZNAM_USER"]
    seznam_pass = os.environ["SEZNAM_PASS"]
    recipient = "martin.kasperlik@rsj.com"

    from datetime import datetime
    body = f"Your morning dashboard is ready:\n\n{dashboard_url}\n"
    msg = MIMEText(body)
    msg["Subject"] = f"Morning Dashboard — {datetime.now().strftime('%b %d, %Y')}"
    msg["From"] = seznam_user
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.seznam.cz", 465) as server:
        server.login(seznam_user, seznam_pass)
        server.sendmail(seznam_user, recipient, msg.as_string())
