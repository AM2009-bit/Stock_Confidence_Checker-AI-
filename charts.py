"""
=========================================================
DipScanner-AI
charts.py
=========================================================

Creates interactive Plotly charts for historical
trading setups.

Outputs:
    output/charts/*.html

Author: Your Name
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import (
    OUTPUT_FOLDER,
    TOP_RESULTS,
    EMA_SHORT,
    EMA_MEDIUM,
    EMA_LONG
)

EMA_SHORT_COL = f"EMA_{EMA_SHORT}"
EMA_MEDIUM_COL = f"EMA_{EMA_MEDIUM}"
EMA_LONG_COL = f"EMA_{EMA_LONG}"


class ChartGenerator:

    def __init__(self):

        self.chart_folder = (

            Path(OUTPUT_FOLDER)

            / "charts"

        )

        self.chart_folder.mkdir(

            parents=True,

            exist_ok=True

        )

    # --------------------------------------------------

    def create_chart(

        self,

        ticker,

        df,

        signal_date

    ):

        signal_date = pd.to_datetime(signal_date)

        signal_index = df.index.get_loc(signal_date)

        start = max(

            signal_index - 30,

            0

        )

        end = min(

            signal_index + 30,

            len(df)-1

        )

        chart = df.iloc[start:end+1]

        fig = make_subplots(

            rows=3,

            cols=1,

            shared_xaxes=True,

            vertical_spacing=0.03,

            row_heights=[0.6,0.2,0.2]

        )

        # ======================================
        # Candlestick
        # ======================================

        fig.add_trace(

            go.Candlestick(

                x=chart.index,

                open=chart["Open"],

                high=chart["High"],

                low=chart["Low"],

                close=chart["Close"],

                name="Price"

            ),

            row=1,

            col=1

        )

        # ======================================
        # EMA Lines
        # ======================================

        fig.add_trace(

            go.Scatter(

                x=chart.index,

                y=chart[EMA_SHORT_COL],

                name=f"EMA {EMA_SHORT}",

                line=dict(width=1)

            ),

            row=1,

            col=1

        )

        fig.add_trace(

            go.Scatter(

                x=chart.index,

                y=chart[EMA_MEDIUM_COL],

                name=f"EMA {EMA_MEDIUM}",

                line=dict(width=1)

            ),

            row=1,

            col=1

        )

        fig.add_trace(

            go.Scatter(

                x=chart.index,

                y=chart[EMA_LONG_COL],

                name=f"EMA {EMA_LONG}",

                line=dict(width=1)

            ),

            row=1,

            col=1

        )

        # ======================================
        # Bollinger Bands
        # ======================================

        fig.add_trace(

            go.Scatter(

                x=chart.index,

                y=chart["BB_UPPER"],

                name="Upper BB",

                line=dict(width=1)

            ),

            row=1,

            col=1

        )

        fig.add_trace(

            go.Scatter(

                x=chart.index,

                y=chart["BB_LOWER"],

                name="Lower BB",

                line=dict(width=1)

            ),

            row=1,

            col=1

        )

        # ======================================
        # Buy Signal
        # ======================================

        price = df.loc[signal_date]["Close"]

        fig.add_trace(

            go.Scatter(

                x=[signal_date],

                y=[price],

                mode="markers",

                marker=dict(

                    size=12,

                    symbol="star"

                ),

                name="Signal"

            ),

            row=1,

            col=1

        )

        # ======================================
        # RSI
        # ======================================

        fig.add_trace(

            go.Scatter(

                x=chart.index,

                y=chart["RSI"],

                name="RSI"

            ),

            row=2,

            col=1

        )

        fig.add_hline(

            y=30,

            row=2,

            col=1

        )

        fig.add_hline(

            y=70,

            row=2,

            col=1

        )

        # ======================================
        # MACD
        # ======================================

        fig.add_trace(

            go.Scatter(

                x=chart.index,

                y=chart["MACD"],

                name="MACD"

            ),

            row=3,

            col=1

        )

        fig.add_trace(

            go.Scatter(

                x=chart.index,

                y=chart["MACD_SIGNAL"],

                name="Signal"

            ),

            row=3,

            col=1

        )

        fig.update_layout(

            title=f"{ticker} | {signal_date.date()}",

            xaxis_rangeslider_visible=False,

            height=900,

            template="plotly_dark"

        )

        filename = (

            self.chart_folder

            /

            f"{ticker}_{signal_date.date()}.html"

        )

        fig.write_html(filename)

    # --------------------------------------------------

    def generate(

        self,

        stock_data,

        opportunities

    ):

        total = min(

            TOP_RESULTS,

            len(opportunities)

        )

        print(

            f"\nGenerating {total} charts..."

        )

        for setup in opportunities[:TOP_RESULTS]:

            ticker = setup["Ticker"]

            df = stock_data[ticker]

            self.create_chart(

                ticker,

                df,

                setup["Date"]

            )

        print(

            "Charts completed."

        )


# ======================================================

if __name__ == "__main__":

    print(

        "Chart Generator Ready."

    )