"""
=========================================================
DipScanner-AI
performance.py
=========================================================

Evaluates historical performance after each detected
trading setup.

Author: Your Name
"""

import pandas as pd


class PerformanceAnalyzer:

    def __init__(self):

        self.periods = [5, 10, 20, 30]

    # --------------------------------------------------

    @staticmethod
    def percent_change(start_price, end_price):

        if start_price == 0:

            return None

        return round(

            ((end_price - start_price) / start_price) * 100,

            2

        )

    # --------------------------------------------------

    def maximum_gain(self, future_prices, entry_price):

        gain = (

            future_prices.max() - entry_price

        ) / entry_price * 100

        return round(gain, 2)

    # --------------------------------------------------

    def maximum_drawdown(self, future_prices, entry_price):

        drawdown = (

            future_prices.min() - entry_price

        ) / entry_price * 100

        return round(drawdown, 2)

    # --------------------------------------------------

    def evaluate_signal(

        self,

        df,

        signal_index

    ):

        results = {}

        entry = df.iloc[signal_index]["Close"]

        for period in self.periods:

            if signal_index + period >= len(df):

                results[f"{period}D Return"] = None

                continue

            exit_price = (

                df.iloc[

                    signal_index + period

                ]["Close"]

            )

            results[f"{period}D Return"] = (

                self.percent_change(

                    entry,

                    exit_price

                )

            )

        horizon = min(

            signal_index + 30,

            len(df) - 1

        )

        # Start the window the day AFTER the signal -- including the
        # entry day itself always contributes a trivial 0% data point
        # to the min/max, which understates real post-signal swings
        # (especially over short horizons near the end of the data).
        window_start = min(signal_index + 1, horizon)

        future = (

            df.iloc[

                window_start:horizon + 1

            ]["Close"]

        )

        results["Maximum Gain"] = (

            self.maximum_gain(

                future,

                entry

            )

        )

        results["Maximum Drawdown"] = (

            self.maximum_drawdown(

                future,

                entry

            )

        )

        return results

    # --------------------------------------------------

    def analyze(

        self,

        stock_data,

        opportunities

    ):

        enhanced = []

        for setup in opportunities:

            ticker = setup["Ticker"]

            date = setup["Date"]

            df = stock_data[ticker]

            try:
                date = pd.to_datetime(date)

                if date not in df.index:
                    continue

                idx = df.index.get_loc(date)

            except KeyError:

                continue

            performance = self.evaluate_signal(

                df,

                idx

            )

            combined = setup.copy()

            combined.update(performance)

            enhanced.append(combined)

        return enhanced


# =====================================================

if __name__ == "__main__":

    print(

        "Performance Analyzer Ready."

    )