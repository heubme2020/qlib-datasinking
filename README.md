# qlib-datasinking — a financial-report data source for Qlib / backtrader

Quant backtests are starved for fundamentals. Price data is everywhere; revenue, net income, and ROE are buried in hundred-page PDFs you have to dig out yourself.

DataSinking already parses full-text filings into clean Markdown (tables intact). This package goes one step further — **three lines to a DataFrame**, ready to feed into Qlib, backtrader, or your own pipeline.

## Install

```bash
pip install qlib-datasinking
```

## Three lines to a DataFrame

```python
from qlib_datasinking import DataSinkingProvider

p = DataSinkingProvider()             # no key = public quota; pass a key to unlock more
dfs = p.tables("300033.SZ", limit=1)  # every table in the latest filing

print(len(dfs))      # e.g. 100+ tables (balance sheet / income statement / cash flow / notes)
print(dfs[2].head()) # the "key financial data" table
```

`tables()` returns tables in document order — the first few are the three financial statements.

## Three examples

The repo's [`examples.py`](https://github.com/heubme2020/qlib-datasinking/blob/main/examples.py) has three runnable examples:

1. **Fetch a filing** and browse its statements.
2. **Peer comparison** — pull the "key financial data" table for three companies side by side.
3. **Fundamental factor → Qlib format** — turn revenue into a `(instrument, datetime, feature, value)` table that `D.features()` consumes.

```python
# example 2: peer comparison (Moutai / Wuliangye / Luzhou Laojiao)
from qlib_datasinking import DataSinkingProvider

p = DataSinkingProvider()
for sym in ["600519.SS", "000858.SZ", "000568.SZ"]:
    dfs = p.tables(sym, limit=1)
    # find the table containing "营业收入" (revenue) and compare
```

## API key, quotas and rate limits

You don't need a key to start, but the public tier is throttled — use a (free) key for real backtests.

| Tier | Quota | Rate limit |
|---|---|---|
| No key (public) | 31 reports / 7 days / IP | ~1 request / 3 s |
| Free key | 8,191 reports / 7 days | 3 requests / s |
| Paid ($31/yr) | 524,287 reports / 7 days | 31 requests / s |

- Quota counts **reports**, not requests — one report = one unit.
- The public tier is for trying it out; a backtest loop will hit the 3 s throttle almost immediately.
- Hit a limit and you get a `QuotaError` carrying the tier table above plus the upgrade link (https://datasink.ing/pricing).

## Supported symbols

US `AAPL` · China `600519.SS` · Japan `7203.T` · Korea `005930.KS` · Taiwan `2330.TW` · UK `VOD.L`

Don't know the ticker? Search by name: `GET https://api.datasink.ing/search?q=Apple`

Covers 6 markets: US, China, Japan, Korea, Taiwan, UK.

## Into Qlib / backtrader

`tables()` and `list_reports()` return plain pandas objects, so plugging them into Qlib's `DatasetH` or backtrader's `bt.feeds.PandasData` is standard fare.

- GitHub: https://github.com/heubme2020/qlib-datasinking
- API docs: https://datasink.ing/docs
