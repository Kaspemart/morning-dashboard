import yfinance as yf


def fetch_data():
    ticker = yf.Ticker("VUAG.L")
    hist = ticker.history(period="max")
    info = ticker.fast_info
    return hist, info
