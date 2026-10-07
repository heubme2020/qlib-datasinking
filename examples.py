"""qlib-datasinking 示例：3 个例子（基础 → 同业对比 → Qlib 因子集成）。

跑法：
    pip install pyqlib pandas requests
    pip install git+https://github.com/heubme2020/qlib-datasinking
    python examples.py

⚠️ 不填 key 走公共额度（约 3 秒/次、7 天 31 篇），多公司示例会自动 sleep 等限流。
    跑回测建议先去 datasink.ing 领免费 key，把 DataSinkingProvider(api_key="...") 填上。
"""
import os

import pandas as pd

from qlib_datasinking import DataSinkingProvider

# 优先读环境变量 DATASINKING_API_KEY；不填则走公共额度（限速 3 秒/篇）
p = DataSinkingProvider(os.environ.get("DATASINKING_API_KEY", ""))


def find_table(dfs, keywords):
    """返回第一张包含任一关键词的表格（拉平所有单元格搜，避开宽表截断 + 重复列名）。

    传中文 + 英文关键词，兼容 A 股公司的「英文版财报」。
    """
    keys = [keywords] if isinstance(keywords, str) else keywords
    for df in dfs:
        for v in df.values.ravel():
            s = str(v)
            if any(k in s for k in keys):
                return df
    return None


def example1_fetch():
    """例 1：拉一份财报，看三大报表长什么样。"""
    print("=" * 70)
    print("例 1：同花顺（300033.SZ）最新一份财报的表格一览")
    dfs = p.tables("300033.SZ", limit=1)
    print(f"共 {len(dfs)} 张表（资产负债表/利润表/现金流量表/附注都在里面）\n")
    for i, df in enumerate(dfs[:6]):
        cols = list(df.columns)[:3]
        print(f"  表{i}: {df.shape[0]} 行 x {df.shape[1]} 列 | 表头: {cols}")
    return dfs


def example2_peers():
    """例 2：同业横向对比——白酒三兄弟的「主要会计数据」。"""
    print("\n" + "=" * 70)
    print("例 2：茅台 / 五粮液 / 泸州老窖 横向对比")
    peers = {"贵州茅台": "600519.SS", "五粮液": "000858.SZ", "泸州老窖": "000568.SZ"}
    for name, sym in peers.items():
        dfs = p.tables(sym, limit=1)
        table = find_table(dfs, ["营业", "Revenue"])  # 主要会计数据表（含营收/净利润/ROE）
        print(f"\n{name}（{sym}）：")
        print(table.head(4).to_string() if table is not None else "  未找到")


def example3_qlib():
    """例 3：基本面因子 → Qlib 的 (instrument, datetime, feature) 长表。"""
    print("\n" + "=" * 70)
    print("例 3：把「营业收入」做成 Qlib 因子")
    try:
        import qlib  # 量化框架：这里用它的因子长表约定
    except ImportError:
        print("  未安装 qlib —— 先 pip install pyqlib 再跑本例子")
        return

    rows = []
    for rep in p.fetch_report("600519.SS", limit=3):
        md = rep.get("content", "")
        # 从 Markdown 里抽「营业收入」那一行的数值（示意：找包含该词的表格）
        dfs = DataSinkingProvider._md_tables(DataSinkingProvider._strip_frontmatter(md))
        table = find_table(dfs, ["营业收入", "Revenue"])
        if table is None:
            continue
        # 找「营业收入」所在行，取它后面第一个数字
        for _, r in table.iterrows():
            if any("营业收入" in str(v) for v in r.values):
                nums = [v for v in r.values if isinstance(v, str) and v.replace(",", "").replace(".", "").isdigit()]
                if nums:
                    rows.append({
                        "instrument": rep.get("symbol"),
                        "datetime": rep.get("report_period"),
                        "feature": "revenue",
                        "value": float(nums[0].replace(",", "")),
                    })
                break

    factor = pd.DataFrame(rows)
    print(factor if not factor.empty else "  （未抽到，字段格式随报告而异，示意）")
    print("\n→ 这张 (instrument, datetime, feature, value) 长表，正是 qlib.init 后")
    print("  D.features(['revenue']) 能直接消费的因子格式。")
    print(f"  qlib 版本：{qlib.__version__}")


if __name__ == "__main__":
    example1_fetch()
    example2_peers()
    example3_qlib()
