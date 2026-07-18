"""
=========================================================
DipScanner-AI
scoring.py
=========================================================

Historical scoring engine.

Scores every qualifying setup within the selected
historical period.

Author: Your Name
"""

import pandas as pd

from config import (
    MAX_RSI,
    MINIMUM_SCORE,
    SUPPORT_LOOKBACK,
    WEIGHTS,
    EMA_SHORT
)

EMA_SHORT_COL = f"EMA_{EMA_SHORT}"


class DipScorer:

    def __init__(self):

        pass

    # --------------------------------------------------

    def calculate_score(self, df, i):

        row = df.iloc[i]

        score = 0

        reasons = []

        # -------------------------------
        # Candlestick Patterns
        # -------------------------------

        if row["Doji"]:

            score += WEIGHTS["doji"]

            reasons.append("Doji")

        if row["Hammer"]:

            score += WEIGHTS["hammer"]

            reasons.append("Hammer")

        if row["Bullish_Engulfing"]:

            score += WEIGHTS["engulfing"]

            reasons.append("Bullish Engulfing")

        if row["Morning_Star"]:

            score += WEIGHTS["morning_star"]

            reasons.append("Morning Star")

        # -------------------------------
        # RSI
        # -------------------------------

        if row["RSI"] <= MAX_RSI:

            score += WEIGHTS["rsi"]

            reasons.append(

                f"RSI {row['RSI']:.1f}"

            )

        # -------------------------------
        # MACD
        # -------------------------------

        if row["MACD"] > row["MACD_SIGNAL"]:

            score += WEIGHTS["macd"]

            reasons.append(

                "Bullish MACD"

            )

        # -------------------------------
        # EMA Trend
        # -------------------------------

        if row["Close"] > row[EMA_SHORT_COL]:

            score += WEIGHTS["ema"]

            reasons.append(

                f"Above EMA{EMA_SHORT}"

            )

        # -------------------------------
        # Volume
        # -------------------------------

        if row["Volume"] > row["VOLUME_MA20"]:

            score += WEIGHTS["volume"]

            reasons.append(

                "High Volume"

            )

        # -------------------------------
        # Support
        # -------------------------------

        if i >= SUPPORT_LOOKBACK:

            support = (

                df["Low"]

                .iloc[

                    i-SUPPORT_LOOKBACK:i

                ]

                .min()

            )

            distance = abs(

                row["Close"] - support

            )

            if support > 0:

                if (

                    distance / support

                ) <= 0.03:

                    score += WEIGHTS["support"]

                    reasons.append(

                        "Near Support"

                    )

        return score, reasons

    # --------------------------------------------------

    def score_history(

        self,

        ticker,

        df

    ):

        opportunities = []

        for i in range(

            SUPPORT_LOOKBACK,

            len(df)

        ):

            score, reasons = (

                self.calculate_score(

                    df,

                    i

                )

            )

            if score < MINIMUM_SCORE:

                continue

            row = df.iloc[i]

            opportunities.append(

                {

                    "Ticker": ticker,

                    "Date": df.index[i],

                    "Score": score,

                    "Close": round(

                        row["Close"],

                        2

                    ),

                    "RSI": round(

                        row["RSI"],

                        2

                    ),

                    "Reasons": reasons

                }

            )

        return opportunities

    # --------------------------------------------------

    def score_latest(

        self,

        ticker,

        df

    ):
        """
        Scores only the most recent bar for a ticker, regardless of
        whether it clears MINIMUM_SCORE. Unlike score_history() (which
        only records days that already qualify as a historical dip
        setup), this always returns a result so every ticker in the
        watchlist gets a current read -- not just the ones currently
        sitting in dip territory.
        """

        if len(df) <= SUPPORT_LOOKBACK:

            return None

        i = len(df) - 1

        score, reasons = self.calculate_score(df, i)

        row = df.iloc[i]

        return {

            "Ticker": ticker,

            "Date": df.index[i],

            "Score": score,

            "Close": round(row["Close"], 2),

            "RSI": round(row["RSI"], 2),

            "Reasons": reasons,

            "Meets Dip Threshold": score >= MINIMUM_SCORE

        }

    # --------------------------------------------------

    def score_all_latest(

        self,

        stock_data

    ):
        """
        Returns one current snapshot per ticker (see score_latest),
        sorted highest score first. Tickers with too little history
        are skipped with a note rather than silently vanishing.
        """

        snapshots = []

        skipped = []

        for ticker, df in stock_data.items():

            snapshot = self.score_latest(ticker, df)

            if snapshot is None:

                skipped.append(ticker)

                continue

            snapshots.append(snapshot)

        snapshots = sorted(

            snapshots,

            key=lambda x: x["Score"],

            reverse=True

        )

        return snapshots, skipped

    # --------------------------------------------------

    def score_all(

        self,

        stock_data

    ):

        all_opportunities = []

        for ticker, df in stock_data.items():

            setups = self.score_history(

                ticker,

                df

            )

            all_opportunities.extend(

                setups

            )

        all_opportunities = sorted(

            all_opportunities,

            key=lambda x: x["Score"],

            reverse=True

        )

        return all_opportunities


# =====================================================

if __name__ == "__main__":

    print(

        "Historical DipScorer Ready."

    )