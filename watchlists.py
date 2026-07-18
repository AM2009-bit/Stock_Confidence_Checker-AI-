"""
DipScanner-AI
watchlists.py
"""

WATCHLISTS = {
    "SP500": [
        "AAPL", "MSFT", "NVDA", "AMZN", "META",
        "GOOGL", "TSLA", "BRK-B", "JPM", "V"
    ],

    "NASDAQ100": [
        "AAPL", "MSFT", "NVDA", "AMZN", "META",
        "GOOGL", "TSLA", "AMD", "NFLX", "AVGO"
    ],

    "DOW30": [
        "AAPL", "MSFT", "JPM", "V", "HD",
        "DIS", "CRM", "KO", "MCD", "CAT"
    ],

    "SEMICONDUCTORS": [
        "NVDA", "AMD", "MU", "AVGO",
        "QCOM", "TXN", "INTC", "ON", "AMAT", "LRCX"
    ],

    "AEROSPACE": [
        "RTX", "LMT", "NOC", "BA",
        "GD", "LHX", "TXT", "HWM", "KTOS"
    ],

    "AI": [
        "NVDA", "AMD", "MSFT", "GOOGL",
        "META", "AMZN", "PLTR", "SMCI"
    ]
}


def get_watchlist(name, custom_watchlist=None):
    """
    Returns the requested watchlist.
    """

    if name == "CUSTOM":
        return custom_watchlist if custom_watchlist else []

    return WATCHLISTS.get(name.upper(), [])