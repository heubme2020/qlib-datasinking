# qlib-datasinking — 财报数据源 for Qlib / backtrader

把上市公司的**财报全文**（资产负债表 / 利润表 / 现金流量表 + 附注）拉成 pandas DataFrame，直接喂给 Qlib、backtrader 或你自己的回测。

## 为什么

量化框架装完只有行情数据，基本面数字（营收、净利润、总资产）得你自己从 PDF/数据库里抠。DataSinking 已经把财报全文转成了干净的 Markdown（表格都在），这个包再进一步——**三步变成 DataFrame**。

## 安装

```bash
pip install qlib-datasinking
```

## 三步拿到 DataFrame

```python
from qlib_datasinking import DataSinkingProvider

p = DataSinkingProvider()          # 不填 key = 公共额度；填 key 解锁更多
dfs = p.tables("600519.SS", limit=1)   # 贵州茅台最新一份财报的所有表格

print(len(dfs))      # 比如 136 张表（资产负债表/利润表/现金流量表/附注）
print(dfs[2].head()) # 「主要会计数据」那张
```

`tables()` 按财报原文顺序返回表格，前几张通常就是三大报表，要哪张取哪张。

## API key / 限额 / 限速（重点）

不填 key 也能用，但公共档有限速，跑回测请用（免费的）key。

| 档位 | 额度 | 限速 | 怎么拿 |
|---|---|---|---|
| 无 key（公共） | 7 天 31 篇 / IP | 约 3 秒 1 次 | 不用拿 |
| 免费 key | 7 天 8,191 篇 | 3 次/秒 | datasink.ing 邮箱领 |
| 付费（$31/年） | 7 天 524,287 篇 | 31 次/秒 | datasink.ing 升级 |

- **额度按「篇」算，不是按请求数**——一份财报 = 一篇。`tables("AAPL", limit=3)` 拉 3 份就是 3 篇。
- **公共档**是给试用的：拉单份没问题，但回测循环一跑就会撞 3 秒限速。
- **免费 key** 是个人量化的甜点档——7 天 8,191 篇够跑多年份、多公司的回测，3 次/秒也比公共限速快约 9 倍。

## 支持

- 代码：美股 `AAPL` / A股 `600519.SS` / 日股 `7203.T` / 韩股 `005930.KS` / 台股 `2330.TW` / 英股 `VOD.L`
- 不知道代码？按公司名搜：`GET https://api.datasink.ing/search?q=Apple`
- 覆盖 6 市场：美 / 中 / 日 / 韩 / 台 / 英

## 喂进回测

`tables()` / `list_reports()` 返回的都是标准 pandas 对象，接进 Qlib 的 `DatasetH` 或 backtrader 的 `bt.feeds.PandasData` 都是常规操作。API 文档见 https://datasink.ing/docs
