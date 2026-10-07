# qlib-datasinking — 财报数据源 for Qlib / backtrader

把上市公司的**财报全文**（资产负债表 / 利润表 / 现金流量表 + 附注）拉成 pandas DataFrame，直接喂给 Qlib、backtrader 或你自己的回测。

## 为什么

量化回测框架最缺的是**基本面数据源**。Qlib 装完只管行情因子，财报数字你得自己从 PDF/数据库里抠。DataSinking 已经把财报全文转成了干净的 Markdown（表格都在），这个包把它再进一步——**三步变成 DataFrame**。

## 安装

```bash
pip install qlib-datasinking
```

## 三步拿到 DataFrame

```python
from qlib_datasinking import DataSinkingProvider

p = DataSinkingProvider()          # 不填 key 走公共额度；填 key 解锁 8191 篇/7 天
dfs = p.tables("600519.SS", limit=1)   # 贵州茅台最新一份财报的所有表格

print(len(dfs))    # 136 张表（资产负债表/利润表/现金流量表/附注…）
print(dfs[2].head())   # 主要会计数据那张
```

`p.tables()` 按财报原文顺序返回表格列表，前三张通常就是三大报表。要哪张取哪张。

## 领 key（推荐）

不填 key 也能用，但公共额度限速（约 3 秒一次、7 天 31 篇），跑回测会撞限流。去 https://datasink.ing 用邮箱领个免费 key（7 天 8,191 篇），填进 `DataSinkingProvider(api_key="...")`。

## 支持

- 代码：美股 `AAPL` / A股 `600519.SS` / 日股 `7203.T` / 韩股 `005930.KS` / 台股 `2330.TW` / 英股 `VOD.L`
- 不知道代码？按公司名搜：`GET https://api.datasink.ing/search?q=Apple`
- 覆盖 6 市场：美 / 中 / 日 / 韩 / 台 / 英

## 喂进回测

`tables()` / `list_reports()` 返回的都是标准 pandas 对象，接进 Qlib 的 `DatasetH` 或 backtrader 的 `bt.feeds.PandasData` 就是常规操作。API 文档见 https://datasink.ing/docs。
