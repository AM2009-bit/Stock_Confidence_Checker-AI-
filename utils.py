"""
=========================================================
DipScanner-AI
utils.py
=========================================================

General utility functions used throughout the project.

Author: Your Name
"""

from pathlib import Path
from datetime import datetime
import logging
import pandas as pd

from config import EMA_SHORT, EMA_MEDIUM, EMA_LONG

EMA_SHORT_COL = f"EMA_{EMA_SHORT}"
EMA_MEDIUM_COL = f"EMA_{EMA_MEDIUM}"
EMA_LONG_COL = f"EMA_{EMA_LONG}"

# =====================================================
# Logging
# =====================================================

def setup_logger():

    logger = logging.getLogger("DipScanner")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "[%(levelname)s] %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


LOGGER = setup_logger()

# =====================================================
# File Helpers
# =====================================================

def ensure_directory(folder):

    Path(folder).mkdir(

        parents=True,

        exist_ok=True

    )


# =====================================================
# Time
# =====================================================

def timestamp():

    return datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )


# =====================================================
# Math Helpers
# =====================================================

def percent_change(old, new):

    if old == 0:

        return None

    return round(

        ((new-old)/old)*100,

        2

    )


def round_price(price):

    return round(

        float(price),

        2

    )


# =====================================================
# Trend
# =====================================================

def market_trend(df):

    latest = df.iloc[-1]

    ema_short = latest[EMA_SHORT_COL]
    ema_medium = latest[EMA_MEDIUM_COL]
    ema_long = latest[EMA_LONG_COL]

    # EMA_LONG (default 200-period) needs at least that many rows of
    # history to produce a real value -- if TIME_PERIOD is too short,
    # this will be NaN and every comparison below silently evaluates
    # to False, always reporting "Sideways" instead of a real signal.
    if pd.isna(ema_short) or pd.isna(ema_medium) or pd.isna(ema_long):
        return "Insufficient Data"

    if ema_short > ema_medium > ema_long:

        return "Strong Bullish"

    if ema_short > ema_medium:

        return "Bullish"

    if ema_short < ema_medium < ema_long:

        return "Strong Bearish"

    return "Sideways"


# =====================================================
# Validation
# =====================================================

def validate_dataframe(df):

    required = [

        "Open",

        "High",

        "Low",

        "Close",

        "Volume"

    ]

    for column in required:

        if column not in df.columns:

            raise ValueError(

                f"Missing column {column}"

            )

    return True


# =====================================================
# Ranking
# =====================================================

def sort_results(results):

    return sorted(

        results,

        key=lambda x: x["Score"],

        reverse=True

    )


# =====================================================
# Statistics
# =====================================================

def average_score(results):

    if len(results) == 0:

        return 0

    scores = [

        r["Score"]

        for r in results

    ]

    return round(

        sum(scores)/len(scores),

        2

    )


def win_rate(results):

    returns = [

        r["30D Return"]

        for r in results

        if r["30D Return"] is not None

    ]

    if len(returns) == 0:

        return 0

    wins = [

        r for r in returns

        if r > 0

    ]

    return round(

        len(wins)/len(returns)*100,

        2

    )


# =====================================================
# Save DataFrame
# =====================================================

def save_dataframe(

    df,

    filename

):

    Path(filename).parent.mkdir(

        parents=True,

        exist_ok=True

    )

    df.to_csv(

        filename,

        index=False

    )


# =====================================================
# Pretty Console
# =====================================================

def divider():

    print("=" * 80)


def header(text):

    divider()

    print(text)

    divider()


# =====================================================
# Quick Test
# =====================================================

if __name__ == "__main__":

    LOGGER.info(

        "Utilities Loaded"

    )

    print(

        timestamp()

    )