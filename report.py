"""
=========================================================
DipScanner-AI
report.py
=========================================================

Creates reports from historical trading setups.

Outputs:
- CSV
- Console summary
- Statistics

Author: Your Name
"""

from pathlib import Path
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from config import (
    OUTPUT_FOLDER,
    TOP_RESULTS,
    GENERATE_CSV,
    GENERATE_PDF
)

from utils import market_trend


class ReportGenerator:

    def __init__(self):

        self.output = Path(OUTPUT_FOLDER)

        self.output.mkdir(

            parents=True,

            exist_ok=True

        )

    # ----------------------------------------------------

    def create_dataframe(self, opportunities):

        if len(opportunities) == 0:

            return pd.DataFrame()

        df = pd.DataFrame(opportunities)

        df = df.sort_values(

            "Score",

            ascending=False

        )

        return df

    # ----------------------------------------------------

    def print_top(self, df):

        print("\n")

        print("=" * 80)

        print("TOP HISTORICAL OPPORTUNITIES")

        print("=" * 80)

        if df.empty:

            print("No qualifying setups found.")

            return

        columns = [

            "Ticker",

            "Date",

            "Score",

            "Close",

            "5D Return",

            "10D Return",

            "20D Return",

            "30D Return"

        ]

        print(

            df[columns]

            .head(TOP_RESULTS)

            .to_string(index=False)

        )

    # ----------------------------------------------------

    def statistics(self, df):

        print("\n")

        print("=" * 80)

        print("SUMMARY")

        print("=" * 80)

        print(

            f"Total Signals : {len(df)}"

        )

        if df.empty:

            return

        print(

            f"Highest Score : {df['Score'].max()}"

        )

        print(

            f"Average Score : {round(df['Score'].mean(),2)}"

        )

        print(

            f"Average 30D Return : "

            f"{round(df['30D Return'].mean(),2)}%"

        )

        print(

            f"Average Max Gain : "

            f"{round(df['Maximum Gain'].mean(),2)}%"

        )

        print(

            f"Average Max Drawdown : "

            f"{round(df['Maximum Drawdown'].mean(),2)}%"

        )

    # ----------------------------------------------------

    def save_csv(self, df):

        if not GENERATE_CSV:

            return

        filename = (

            self.output /

            "historical_opportunities.csv"

        )

        df.to_csv(

            filename,

            index=False

        )

        print(

            f"\nSaved CSV -> {filename}"

        )

    # ----------------------------------------------------

    def save_pdf(self, df):

        if not GENERATE_PDF:

            return

        if df.empty:

            return

        filename = (

            self.output /

            "historical_opportunities.pdf"

        )

        doc = SimpleDocTemplate(

            str(filename),

            pagesize=landscape(letter)

        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(

            Paragraph("DipScanner-AI Report", styles["Title"])

        )

        elements.append(Spacer(1, 12))

        # -------------------------------
        # Summary section
        # -------------------------------

        summary_lines = [

            f"Total Signals: {len(df)}",

            f"Highest Score: {df['Score'].max()}",

            f"Average Score: {round(df['Score'].mean(), 2)}",

        ]

        if "30D Return" in df.columns:

            summary_lines.append(

                f"Average 30D Return: {round(df['30D Return'].mean(), 2)}%"

            )

        if "Maximum Gain" in df.columns:

            summary_lines.append(

                f"Average Max Gain: {round(df['Maximum Gain'].mean(), 2)}%"

            )

        if "Maximum Drawdown" in df.columns:

            summary_lines.append(

                f"Average Max Drawdown: {round(df['Maximum Drawdown'].mean(), 2)}%"

            )

        for line in summary_lines:

            elements.append(Paragraph(line, styles["Normal"]))

        elements.append(Spacer(1, 18))

        # -------------------------------
        # Top opportunities table
        # -------------------------------

        elements.append(

            Paragraph("Top Historical Opportunities", styles["Heading2"])

        )

        elements.append(Spacer(1, 8))

        columns = [

            "Ticker",

            "Date",

            "Score",

            "Close",

            "5D Return",

            "10D Return",

            "20D Return",

            "30D Return"

        ]

        columns = [c for c in columns if c in df.columns]

        table_df = df[columns].head(TOP_RESULTS).copy()

        # Dates render more cleanly as plain strings in the PDF table
        if "Date" in table_df.columns:

            table_df["Date"] = table_df["Date"].astype(str)

        table_data = [columns] + table_df.values.tolist()

        table = Table(table_data, repeatRows=1)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#222222")),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("FONTSIZE", (0, 0), (-1, -1), 8),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),

            ])

        )

        elements.append(table)

        doc.build(elements)

        print(

            f"\nSaved PDF -> {filename}"

        )

    # ----------------------------------------------------

    def print_snapshot(self, snapshots, skipped, stock_data):

        print("\n")

        print("=" * 80)

        print("CURRENT SNAPSHOT (Score + Position, every watchlist ticker)")

        print("=" * 80)

        if not snapshots:

            print("No snapshots available.")

            return

        for s in snapshots:

            trend = market_trend(stock_data[s["Ticker"]])

            dip_flag = " [DIP SETUP]" if s["Meets Dip Threshold"] else ""

            factors = ", ".join(s["Reasons"]) if s["Reasons"] else "None"

            print(

                f"\n{s['Ticker']:<6} | Score: {s['Score']:>3}/100 | "
                f"Position: {trend}{dip_flag}"

            )

            print(f"       Close: {s['Close']}  |  RSI: {s['RSI']}")

            print(f"       Best Factors: {factors}")

        if skipped:

            print(

                "\nSkipped (insufficient history for a reliable score): "
                + ", ".join(skipped)

            )

    # ----------------------------------------------------

    def save_snapshot_csv(self, snapshots, stock_data):

        if not GENERATE_CSV:

            return

        if not snapshots:

            return

        rows = []

        for s in snapshots:

            trend = market_trend(stock_data[s["Ticker"]])

            rows.append({

                "Ticker": s["Ticker"],

                "Date": s["Date"],

                "Score": s["Score"],

                "Position": trend,

                "Close": s["Close"],

                "RSI": s["RSI"],

                "Meets Dip Threshold": s["Meets Dip Threshold"],

                "Best Factors": ", ".join(s["Reasons"]) if s["Reasons"] else ""

            })

        df = pd.DataFrame(rows)

        filename = self.output / "current_snapshot.csv"

        df.to_csv(filename, index=False)

        print(f"\nSaved Snapshot CSV -> {filename}")

    # ----------------------------------------------------

    def best_signals(self, df):

        if df.empty:

            return

        print("\n")

        print("=" * 80)

        print("TOP 10 SCORES")

        print("=" * 80)

        cols = [

            "Ticker",

            "Date",

            "Score",

            "Maximum Gain",

            "Maximum Drawdown"

        ]

        print(

            df[cols]

            .head(10)

            .to_string(index=False)

        )

    # ----------------------------------------------------

    def generate(self, opportunities):

        df = self.create_dataframe(

            opportunities

        )

        self.print_top(df)

        self.statistics(df)

        self.best_signals(df)

        self.save_csv(df)

        self.save_pdf(df)

        return df


# ========================================================

if __name__ == "__main__":

    print(

        "Report Generator Ready."

    )