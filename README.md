# DipScanner-AI

A lightweight Python application that scans historical stock data to
identify potential dip-buy opportunities using candlestick patterns
and technical indicators. Default lookback is 2 years (configurable
in `config.py`), which gives the 200-period EMA/SMA enough history to
actually compute (a shorter window like 6 months leaves those always
`NaN`).

## Features

-   Historical stock scanner with local CSV caching and a liquidity
    filter (skips tickers below `MIN_AVERAGE_VOLUME`)
-   Doji, Hammer, Bullish Engulfing, and Morning Star candlestick
    detection
-   RSI, EMA, SMA, MACD, Bollinger Bands, ATR
-   Weighted confidence scoring
-   Historical performance analysis (5/10/20/30-day forward returns,
    max gain, max drawdown per signal)
-   Interactive Plotly candlestick charts per signal
-   CSV and PDF report export

## Project Structure

    DipScanner-AI/
    README.md
    requirements.txt
    .gitignore
    main.py
    config.py
    scanner.py
    indicators.py
    patterns.py
    scoring.py
    performance.py
    report.py
    charts.py
    utils.py
    watchlists.py
    data/
    output/

## Installation

``` bash
python -m venv .venv
source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

> **Note:** `requirements.txt` pins `numpy<2.0.0`. The pinned
> `pandas-ta` release relies on the `numpy.NaN` alias, which was
> removed in NumPy 2.0 -- installing NumPy 2.x will break
> `import pandas_ta` immediately.

## Workflow

1.  Download historical data (cached locally for 24 hours).
2.  Filter out illiquid tickers.
3.  Calculate indicators.
4.  Detect candlestick patterns.
5.  Score historical setups.
6.  Analyze forward performance of each setup.
7.  Export CSV/PDF reports and per-signal charts.

## Disclaimer

Educational purposes only. Not financial advice.

