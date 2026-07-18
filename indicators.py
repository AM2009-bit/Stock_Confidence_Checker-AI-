"""
=================================================
DipScanner-AI
indicators.py
=================================================

Calculates all technical indicators used by the
scanner.

Author: Your Name
"""

import pandas as pd
import pandas_ta as ta

from config import (
    RSI_PERIOD,
    EMA_SHORT,
    EMA_MEDIUM,
    EMA_LONG,
    MACD_FAST,
    MACD_SLOW,
    MACD_SIGNAL,
    BOLLINGER_PERIOD,
    BOLLINGER_STD,
    ATR_PERIOD
)


class IndicatorEngine:

    def __init__(self):
        pass

    # ----------------------------------------

    def calculate_rsi(self, df):

        df["RSI"] = ta.rsi(
            df["Close"],
            length=RSI_PERIOD
        )

        return df

    # ----------------------------------------

    def calculate_ema(self, df):

        df[f"EMA_{EMA_SHORT}"] = ta.ema(
            df["Close"],
            length=EMA_SHORT
        )

        df[f"EMA_{EMA_MEDIUM}"] = ta.ema(
            df["Close"],
            length=EMA_MEDIUM
        )

        df[f"EMA_{EMA_LONG}"] = ta.ema(
            df["Close"],
            length=EMA_LONG
        )

        return df

    # ----------------------------------------

    def calculate_macd(self, df):

        macd = ta.macd(
            df["Close"],
            fast=MACD_FAST,
            slow=MACD_SLOW,
            signal=MACD_SIGNAL
        )

        # pandas_ta names these columns MACD_*, MACDh_* (histogram),
        # MACDs_* (signal line) -- in that order. Matching by name
        # prefix (not position, and not a reconstructed suffix that
        # could drift from the library's actual formatting) avoids
        # silently mixing up the signal and histogram series.
        macd_col = next(c for c in macd.columns if c.startswith("MACD_"))
        signal_col = next(c for c in macd.columns if c.startswith("MACDs_"))
        hist_col = next(c for c in macd.columns if c.startswith("MACDh_"))

        df["MACD"] = macd[macd_col]
        df["MACD_SIGNAL"] = macd[signal_col]
        df["MACD_HIST"] = macd[hist_col]

        return df

    # ----------------------------------------

    def calculate_bollinger(self, df):

        bb = ta.bbands(
            df["Close"],
            length=BOLLINGER_PERIOD,
            std=BOLLINGER_STD
        )

        # pandas_ta orders these columns Lower, Middle, Upper
        # (BBL, BBM, BBU) -- matching by name prefix avoids the
        # classic mistake of assuming Upper/Middle/Lower by position.
        lower_col = next(c for c in bb.columns if c.startswith("BBL_"))
        middle_col = next(c for c in bb.columns if c.startswith("BBM_"))
        upper_col = next(c for c in bb.columns if c.startswith("BBU_"))

        df["BB_LOWER"] = bb[lower_col]
        df["BB_MIDDLE"] = bb[middle_col]
        df["BB_UPPER"] = bb[upper_col]

        return df

    # ----------------------------------------

    def calculate_atr(self, df):

        df["ATR"] = ta.atr(
            df["High"],
            df["Low"],
            df["Close"],
            length=ATR_PERIOD
        )

        return df

    # ----------------------------------------

    def calculate_volume_average(self, df):

        df["VOLUME_MA20"] = (
            df["Volume"]
            .rolling(20)
            .mean()
        )

        return df

    # ----------------------------------------

    def calculate_sma(self, df):

        df["SMA20"] = ta.sma(
            df["Close"],
            length=20
        )

        df["SMA50"] = ta.sma(
            df["Close"],
            length=50
        )

        df["SMA200"] = ta.sma(
            df["Close"],
            length=200
        )

        return df

    # ----------------------------------------

    def add_all_indicators(self, df):

        df = self.calculate_rsi(df)

        df = self.calculate_ema(df)

        df = self.calculate_sma(df)

        df = self.calculate_macd(df)

        df = self.calculate_bollinger(df)

        df = self.calculate_atr(df)

        df = self.calculate_volume_average(df)

        return df


# ===========================================
# Quick Test
# ===========================================

if __name__ == "__main__":

    import yfinance as yf

    stock = yf.download(
        "AAPL",
        period="6mo",
        progress=False
    )

    engine = IndicatorEngine()

    stock = engine.add_all_indicators(stock)

    print(stock.tail())