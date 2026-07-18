"""
=========================================================
DipScanner-AI
config.py
=========================================================

Global configuration settings.

Modify this file to customize the scanner.

Author: Your Name
"""

# ======================================================
# DATA SETTINGS
# ======================================================

TIME_PERIOD = "2y"

# NOTE: TIME_PERIOD must comfortably exceed your longest indicator
# period (EMA_LONG / SMA200 = 200 by default). "6mo" (~126 trading
# days) is NOT enough data for a 200-period EMA/SMA to ever produce a
# real value -- every value stays NaN for the whole scan, silently
# breaking market_trend() in utils.py and the EMA_200 line on charts.
# "2y" (~500 trading days) gives a solid buffer above 200. If you
# shorten EMA_LONG below, you can shorten this accordingly.

INTERVAL = "1d"

USE_CACHE = True

CACHE_FOLDER = "data/cache"

OUTPUT_FOLDER = "output"

# ======================================================
# WATCHLIST SETTINGS
# ======================================================

# Options:
#
# "SP500"
# "NASDAQ100"
# "DOW30"
# "SEMICONDUCTORS"
# "AEROSPACE"
# "AI"
# "CUSTOM"

ACTIVE_WATCHLIST = "SP500"

# Used only if ACTIVE_WATCHLIST == "CUSTOM"

CUSTOM_WATCHLIST = [

    "AAPL",

    "MSFT",

    "NVDA",

    "AMD",

    "TSLA"

]

# ======================================================
# TECHNICAL INDICATORS
# ======================================================

RSI_PERIOD = 14

EMA_SHORT = 20
EMA_MEDIUM = 50
EMA_LONG = 200

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

ATR_PERIOD = 14

BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

# ======================================================
# CANDLESTICK PATTERNS
# ======================================================

# A candle is considered a Doji if its body is
# 10% or less of the total candle range.
DOJI_BODY_PERCENT = 0.10

# ======================================================
# SCORING
# ======================================================

MINIMUM_SCORE = 70

MAX_RSI = 35

SUPPORT_LOOKBACK = 20

# Reserved for a future resistance-based scoring rule; not currently
# used anywhere in the scoring engine.
RESISTANCE_LOOKBACK = 20

# ======================================================
# FILTERS
# ======================================================

# MIN_AVERAGE_VOLUME is enforced in scanner.py (tickers whose recent
# average daily volume falls below this are skipped before scoring).

MIN_AVERAGE_VOLUME = 1_000_000

# MIN_MARKET_CAP and IGNORE_EARNINGS_WEEK are NOT yet wired into the
# scanner. Market cap requires a separate per-ticker metadata call
# (yfinance's .info), which is slow and rate-limited, so it's left as
# a placeholder for a future enhancement rather than silently ignored
# without a note. Same for earnings-week detection.

MIN_MARKET_CAP = 10_000_000_000

IGNORE_EARNINGS_WEEK = False

# ======================================================
# REPORT
# ======================================================

GENERATE_CSV = True

GENERATE_PDF = True

GENERATE_CHARTS = True

TOP_RESULTS = 25

# ======================================================
# SCORE WEIGHTS
# ======================================================

WEIGHTS = {

    "doji":20,

    "hammer":10,

    "engulfing":10,

    "morning_star":10,

    "rsi":15,

    "support":15,

    "volume":10,

    "macd":5,

    "ema":5

}