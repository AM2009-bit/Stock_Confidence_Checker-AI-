"""
=================================================
DipScanner-AI
patterns.py
=================================================

Detects bullish candlestick patterns used by
DipScanner-AI.

Author: Your Name
"""

import pandas as pd
from config import DOJI_BODY_PERCENT


class PatternDetector:
    """
    Detects candlestick reversal patterns.
    """

    def __init__(self):
        pass

    # =====================================================
    # Helper Functions
    # =====================================================

    @staticmethod
    def body_size(row):

        return abs(row["Close"] - row["Open"])

    @staticmethod
    def candle_range(row):

        return row["High"] - row["Low"]

    @staticmethod
    def upper_shadow(row):

        return row["High"] - max(row["Open"], row["Close"])

    @staticmethod
    def lower_shadow(row):

        return min(row["Open"], row["Close"]) - row["Low"]

    # =====================================================
    # Doji
    # =====================================================

    def is_doji(self, row):

        rng = self.candle_range(row)

        if rng == 0:
            return False

        body = self.body_size(row)

        return (body / rng) <= DOJI_BODY_PERCENT

    # =====================================================
    # Hammer
    # =====================================================

    def is_hammer(self, row):

        body = self.body_size(row)

        upper = self.upper_shadow(row)

        lower = self.lower_shadow(row)

        if body == 0:
            return False

        return (

            lower >= body * 2

            and

            upper <= body * 0.5

        )

    # =====================================================
    # Bullish Engulfing
    # =====================================================

    def is_bullish_engulfing(self, prev, curr):

        previous_red = prev["Close"] < prev["Open"]

        current_green = curr["Close"] > curr["Open"]

        engulf = (

            curr["Open"] < prev["Close"]

            and

            curr["Close"] > prev["Open"]

        )

        return (

            previous_red

            and

            current_green

            and

            engulf

        )

    # =====================================================
    # Morning Star
    # =====================================================

    def is_morning_star(self, df, i):

        if i < 2:
            return False

        first = df.iloc[i - 2]

        second = df.iloc[i - 1]

        third = df.iloc[i]

        large_red = first["Close"] < first["Open"]

        small_body = (

            self.body_size(second)

            <

            self.body_size(first) * 0.5

        )

        strong_green = third["Close"] > third["Open"]

        recovery = (

            third["Close"]

            >

            (first["Open"] + first["Close"]) / 2

        )

        return (

            large_red

            and

            small_body

            and

            strong_green

            and

            recovery

        )

    # =====================================================
    # Add Pattern Columns
    # =====================================================

    def detect_patterns(self, df):

        df = df.copy()

        df["Doji"] = False

        df["Hammer"] = False

        df["Bullish_Engulfing"] = False

        df["Morning_Star"] = False

        for i in range(len(df)):

            row = df.iloc[i]

            df.at[df.index[i], "Doji"] = self.is_doji(row)

            df.at[df.index[i], "Hammer"] = self.is_hammer(row)

            if i >= 1:

                prev = df.iloc[i - 1]

                df.at[df.index[i], "Bullish_Engulfing"] = (

                    self.is_bullish_engulfing(prev, row)

                )

            if i >= 2:

                df.at[df.index[i], "Morning_Star"] = (

                    self.is_morning_star(df, i)

                )

        return df


# =========================================================
# Quick Test
# =========================================================

if __name__ == "__main__":

    import yfinance as yf

    stock = yf.download(

        "AAPL",

        period="6mo",

        progress=False

    )

    detector = PatternDetector()

    stock = detector.detect_patterns(stock)

    print(

        stock[

            [

                "Doji",

                "Hammer",

                "Bullish_Engulfing",

                "Morning_Star"

            ]

        ].tail(20)

    )