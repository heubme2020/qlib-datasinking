# qlib-datasinking — a financial-report data source for Qlib / backtrader

Turn full-text financial reports (balance sheet, income statement, cash flow + notes) into pandas DataFrames you can feed straight into Qlib, backtrader, or your own backtest.

## Why

Quant frameworks ship with price data and little else. Fundamental numbers — revenue, net income, total assets — you're left to scrape out of PDFs yourself. DataSinking already parses full-text filings into clean Markdown (tables intact); this package takes it one step further — **three lines to a DataFrame**.

## Install

```bash
pip install qlib-datasinking
```

## Three lines to a DataFrame

```python
from qlib_datasinking import DataSinkingProvider

p = DataSinkingProvider()               # no key = public quota; pass a key to unlock more
dfs = p.tables("600519.SS", limit=1)    # every table in Moutai's latest filing

print(len(dfs))      # e.g. 136 tables (balance sheet / income statement / cash flow / notes)
print(dfs[2].head()) # the "key financial data" table
```

`tables()` returns tables in document order — the first few are the three financial statements. Grab the one you need.

## API key, quotas and rate limits

You don't need a key to start, but the public tier is throttled — use a (free) key for real backtests.

| Tier | Quota | Rate limit | How to get |
|---|---|---|---|
| No key (public) | 31 reports / 7 days / IP | ~1 request / 3 s | nothing |
| Free key | 8,191 reports / 7 days | 3 requests / s | email signup at datasink.ing |
| Paid ($31/yr) | 524,287 reports / 7 days | 31 requests / s | upgrade at datasink.ing |

- **Quota counts reports, not requests** — one report = one unit. `tables("AAPL", limit=3)` pulls 3 reports and costs 3 units.
- **Public tier** is for trying it out: fetching a single report is fine, a backtest loop will hit the 3 s throttle almost immediately.
- **Free key** is the sweet spot for personal quant work — 8,191 reports / 7 days covers multi-year, multi-company backtests, and 3 req/s is ~9× the public throttle.

## Supported symbols

US `AAPL` · China `600519.SS` · Japan `7203.T` · Korea `005930.KS` · Taiwan `2330.TW` · UK `VOD.L`

Don't know the ticker? Search by name: `GET https://api.datasink.ing/search?q=Apple`

Covers 6 markets: US, China, Japan, Korea, Taiwan, UK.

## Into a backtest

`tables()` and `list_reports()` return plain pandas objects, so plugging them into Qlib's `DatasetH` or backtrader's `bt.feeds.PandasData` is standard fare. API docs: https://datasink.ing/docs
