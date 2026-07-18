"""
=========================================================
DipScanner-AI
main.py
=========================================================

Main entry point for DipScanner-AI.

Author: Your Name
"""

from config import (
    ACTIVE_WATCHLIST,
    CUSTOM_WATCHLIST,
    GENERATE_CHARTS
)

from scanner import StockScanner
from indicators import IndicatorEngine
from patterns import PatternDetector
from scoring import DipScorer
from performance import PerformanceAnalyzer
from report import ReportGenerator
from charts import ChartGenerator


def main():

    print("=" * 70)
    print("DipScanner-AI")
    print("Historical Technical Analysis Scanner")
    print("=" * 70)

    # -------------------------------------------------
    # Download historical data
    # -------------------------------------------------

    scanner = StockScanner(
        watchlist_name=ACTIVE_WATCHLIST,
        custom_watchlist=CUSTOM_WATCHLIST
    )

    stock_data = scanner.scan()

    if not stock_data:
        print("No market data downloaded.")
        return

    # -------------------------------------------------
    # Calculate Indicators
    # -------------------------------------------------

    indicator_engine = IndicatorEngine()

    print("\nCalculating indicators...")

    for ticker in stock_data:

        stock_data[ticker] = indicator_engine.add_all_indicators(
            stock_data[ticker]
        )

    # -------------------------------------------------
    # Detect Candlestick Patterns
    # -------------------------------------------------

    detector = PatternDetector()

    print("Detecting candlestick patterns...")

    for ticker in stock_data:

        stock_data[ticker] = detector.detect_patterns(
            stock_data[ticker]
        )

    # -------------------------------------------------
    # Historical Scoring
    # -------------------------------------------------

    scorer = DipScorer()

    print("Scoring historical opportunities...")

    opportunities = scorer.score_all(stock_data)

    print(
        f"Found {len(opportunities)} qualifying setups."
    )

    # -------------------------------------------------
    # Current Snapshot (every ticker, right now)
    # -------------------------------------------------
    # Unlike the historical scan above, this always scores every
    # ticker's most recent bar -- regardless of whether it clears
    # MINIMUM_SCORE -- so you get a score + position for each stock
    # in the watchlist, not just the ones currently in dip territory.

    print("Scoring current snapshot for each ticker...")

    snapshots, skipped_snapshot = scorer.score_all_latest(stock_data)

    # -------------------------------------------------
    # Historical Performance
    # -------------------------------------------------

    analyzer = PerformanceAnalyzer()

    print("Analyzing historical performance...")

    opportunities = analyzer.analyze(
        stock_data,
        opportunities
    )

    # -------------------------------------------------
    # Reports
    # -------------------------------------------------

    reporter = ReportGenerator()

    print("Generating report...")

    reporter.print_snapshot(snapshots, skipped_snapshot, stock_data)

    reporter.save_snapshot_csv(snapshots, stock_data)

    report_df = reporter.generate(
        opportunities
    )

    # -------------------------------------------------
    # Charts
    # -------------------------------------------------

    if GENERATE_CHARTS:

        chart_generator = ChartGenerator()

        chart_generator.generate(
            stock_data,
            opportunities
        )

    # -------------------------------------------------
    # Finished
    # -------------------------------------------------

    print("\n")
    print("=" * 70)
    print("Scan Complete")
    print("=" * 70)

    print(f"Stocks Scanned : {len(stock_data)}")
    print(f"Signals Found  : {len(opportunities)}")

    print("\nOutput Folder:")

    print("output/")

    print("  current_snapshot.csv")

    print("  historical_opportunities.csv")

    if GENERATE_CHARTS:
        print("  charts/")

    print("\nDone.")


if __name__ == "__main__":
    main()