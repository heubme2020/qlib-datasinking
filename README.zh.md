# qlib-datasinking：把财报全文变成 Qlib / backtrader 的数据源

量化回测最缺的不是行情，而是基本面数据。营收、净利润、ROE 这些数字散在几百页 PDF 里，得你自己去抠。

DataSinking 已经把财报全文转成了干净的 Markdown（表格都在），`qlib-datasinking` 再进一步——**三步变成 DataFrame，直接喂给 Qlib、backtrader 或你自己的回测**。

## 安装

```bash
pip install git+https://github.com/heubme2020/qlib-datasinking
```

例 3 还需要 Qlib：`pip install pyqlib`。

## 三步拿到 DataFrame

```python
from qlib_datasinking import DataSinkingProvider

p = DataSinkingProvider()             # 不填 key = 公共额度；填 key 解锁更多
dfs = p.tables("300033.SZ", limit=1)  # 同花顺最新一份财报的所有表格

print(len(dfs))      # 比如 100+ 张表（资产负债表/利润表/现金流量表/附注）
print(dfs[2].head()) # 「主要会计数据」那张
```

`tables()` 按财报原文顺序返回表格，前几张通常就是三大报表，要哪张取哪张。

## 三个例子

仓库里的 [`examples.py`](https://github.com/heubme2020/qlib-datasinking/blob/main/examples.py) 有三个可直接跑的例子。把 key 设成环境变量再跑：

```bash
# Linux / macOS
export DATASINKING_API_KEY=你的免费key
python examples.py

# Windows（PowerShell）
$env:DATASINKING_API_KEY="你的免费key"; python examples.py
```

1. **拉财报看三大报表**（同花顺 300033.SZ）
2. **同业横向对比**（茅台 / 五粮液 / 泸州老窖的「主要会计数据」）
3. **基本面因子 → Qlib 因子格式**（把营业收入做成 `instrument/datetime/feature/value` 长表，`D.features()` 能直接消费）

```python
# 例 2：同业对比
from qlib_datasinking import DataSinkingProvider

p = DataSinkingProvider()
for sym in ["600519.SS", "000858.SZ", "000568.SZ"]:
    dfs = p.tables(sym, limit=1)
    # 找含「营业」/「Revenue」的那张表，横向对比
```

## API key / 限额 / 限速

不填 key 也能用，但公共档限速，跑回测请用（免费的）key。

| 档位 | 额度 | 限速 |
|---|---|---|
| 无 key（公共） | 7 天 31 篇 / IP | 约 3 秒 1 次 |
| 免费 key | 7 天 8,191 篇 | 3 次/秒 |
| 付费 $31/年 | 7 天 524,287 篇 | 31 次/秒 |

- 额度按「篇」算，不是按请求数——一份财报 = 一篇。
- 公共档只够试单份；回测循环一跑就会撞 3 秒限速。
- 撞限速/额度时抛 `QuotaError`，提示里带上面三档明细 + 升级链接（https://datasink.ing/pricing）。

## 支持

- 代码：美股 `AAPL` / A股 `600519.SS` / 日股 `7203.T` / 韩股 `005930.KS` / 台股 `2330.TW` / 英股 `VOD.L`
- 不知道代码？按公司名搜：`GET https://api.datasink.ing/search?q=Apple`
- 覆盖 6 市场：美 / 中 / 日 / 韩 / 台 / 英

## 接进 Qlib / backtrader

`tables()` / `list_reports()` 返回标准 pandas 对象，接进 Qlib 的 `DatasetH` 或 backtrader 的 `bt.feeds.PandasData` 是常规操作。

- GitHub：https://github.com/heubme2020/qlib-datasinking
- API 文档：https://datasink.ing/docs

## 常见问题

装 `pyqlib` 可能把 numpy 拉到 2.x，之后 `import pandas` 时若看到 `bottleneck` 的 `_ARRAY_API` 警告，是**无害的**——pandas 会自动回退到纯 Python 路径，不影响使用。
