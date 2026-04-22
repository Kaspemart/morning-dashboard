import yfinance as yf


def fetch_data():
    ticker = yf.Ticker("VUAG.L")
    hist = ticker.history(period="1y")
    info = ticker.fast_info
    return hist, info


def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return (100 - (100 / (1 + rs))).iloc[-1]
