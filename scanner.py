"""
=========================================================
DipScanner-AI
scanner.py
=========================================================

Downloads historical market data, caches it locally,
and returns a dictionary of DataFrames.

Author: Your Name
"""

from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

from config import (
    TIME_PERIOD,
    INTERVAL,
    CACHE_FOLDER,
    USE_CACHE,
    MIN_AVERAGE_VOLUME
)

from watchlists import (
    get_watchlist
)


class StockScanner:

    def __init__(
        self,
        watchlist_name,
        custom_watchlist=None
    ):

        self.watchlist = get_watchlist(

            watchlist_name,

            custom_watchlist

        )

        self.cache = Path(CACHE_FOLDER)

        self.cache.mkdir(

            parents=True,

            exist_ok=True

        )

    # ---------------------------------------------------

    def cache_file(self, ticker):

        return self.cache / f"{ticker}.csv"

    # ---------------------------------------------------

    def cache_exists(self, ticker):

        return self.cache_file(ticker).exists()

    # ---------------------------------------------------

    def cache_recent(self, ticker):

        file = self.cache_file(ticker)

        if not file.exists():

            return False

        modified = datetime.fromtimestamp(

            file.stat().st_mtime

        )

        return (

            datetime.now() - modified

        ) < timedelta(hours=24)

    # ---------------------------------------------------

    def load_cache(self, ticker):

        df = pd.read_csv(
            self.cache_file(ticker),
            index_col=0,
            parse_dates=True
        )

        # Convert columns back to numeric
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        return df

    # ---------------------------------------------------

    def save_cache(self, ticker, df):

        df.to_csv(
            self.cache_file(ticker),
            index_label="Date"
        )

    # ---------------------------------------------------

    def download(self, ticker):

        df = yf.download(
            ticker,
            period=TIME_PERIOD,
            interval=INTERVAL,
            auto_adjust=True,
            progress=False
        )

        if df.empty:
            raise ValueError(f"No data for {ticker}")

        # Flatten MultiIndex columns (newer yfinance)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Keep only needed columns
        required = ["Open", "High", "Low", "Close", "Volume"]

        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df = df[required].copy()

        # Force numeric types
        for col in required:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        return df

    # ---------------------------------------------------

    def get_stock(self, ticker):

        if (

            USE_CACHE

            and

            self.cache_exists(ticker)

            and

            self.cache_recent(ticker)

        ):

            return self.load_cache(

                ticker

            )

        df = self.download(

            ticker

        )

        self.save_cache(

            ticker,

            df

        )

        return df

    # ---------------------------------------------------

    def passes_volume_filter(self, df):
        """
        Skips illiquid tickers whose recent average daily volume
        falls below MIN_AVERAGE_VOLUME. Uses the last 20 trading
        days so a single unusually quiet/active day doesn't decide
        the outcome.
        """

        if len(df) < 20:
            return False

        recent_avg_volume = df["Volume"].tail(20).mean()

        return recent_avg_volume >= MIN_AVERAGE_VOLUME

    # ---------------------------------------------------

    def scan(self):

        results = {}

        failed = []

        skipped_illiquid = []

        total = len(self.watchlist)

        print(f"\nScanning {total} stocks...\n")

        for i, ticker in enumerate(

            self.watchlist,

            start=1

        ):

            print(

                f"[{i}/{total}] {ticker}"

            )

            try:

                df = self.get_stock(ticker)

                if not self.passes_volume_filter(df):

                    skipped_illiquid.append(ticker)

                    continue

                results[ticker] = df


            except Exception as e:

                print(f"\nERROR for {ticker}: {e}")

                failed.append(ticker)

        print("\nFinished.\n")

        print(

            f"Successful: {len(results)}"

        )

        print(

            f"Failed: {len(failed)}"

        )

        print(

            f"Skipped (below MIN_AVERAGE_VOLUME): {len(skipped_illiquid)}"

        )

        if failed:

            print(

                "\nFailed Tickers:"

            )

            print(

                ", ".join(failed)

            )

        if skipped_illiquid:

            print(

                "\nSkipped (Illiquid) Tickers:"

            )

            print(

                ", ".join(skipped_illiquid)

            )

        return results


# =====================================================
# Quick Test
# =====================================================

if __name__ == "__main__":

    scanner = StockScanner(

        watchlist_name="SEMICONDUCTORS"

    )

    stocks = scanner.scan()

    print(

        list(stocks.keys())

    )