"""DataSinkingProvider — fetch full-text financial reports and turn them into DataFrames.

Usage:
    from qlib_datasinking import DataSinkingProvider

    p = DataSinkingProvider(api_key="...")   # leave empty for the public quota
    dfs = p.tables("600519.SS", limit=3)      # balance sheet / income statement / cash flow
"""
import re
from typing import List

import pandas as pd
import requests


class DataSinkingProvider:
    """Data source backed by DataSinking (https://datasink.ing).

    Leave ``api_key`` empty to use the public quota (31 docs / 7 days / IP);
    pass a free key to unlock 8,191 docs / 7 days.
    """

    BASE = "https://api.datasink.ing"

    def __init__(self, api_key: str = ""):
        self.api_key = (api_key or "").strip()

    def _get(self, path: str, params: dict, timeout: int = 60) -> dict:
        r = requests.get(f"{self.BASE}{path}", params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()

    def list_reports(self, symbol: str, limit: int = 10) -> List[dict]:
        """Report metadata for a symbol, newest first."""
        if self.api_key:
            data = self._get("/documents", {
                "symbol": symbol, "order": "desc", "size": limit, "apikey": self.api_key,
            })
        else:
            data = self._get("/public/documents", {
                "symbol": symbol, "order": "desc", "size": limit,
            })
        return data.get("items", [])

    def fetch_report(self, symbol: str, limit: int = 1) -> List[dict]:
        """Full-text reports (Markdown) for a symbol, newest first."""
        if self.api_key:
            data = self._get("/documents", {
                "symbol": symbol, "order": "desc", "size": limit,
                "with_content": 1, "apikey": self.api_key,
            }, timeout=120)
            return data.get("items", [])
        # 无 key：公共端点两步（列表 → 按 id 取全文）
        out: List[dict] = []
        for meta in self.list_reports(symbol, limit):
            out.append(self._get(f"/public/documents/{meta['id']}", {}))
        return out

    def tables(self, symbol: str, limit: int = 1) -> List[pd.DataFrame]:
        """Every Markdown table across the latest ``limit`` reports, as DataFrames.

        Order follows the report text: balance sheet, income statement, cash flow, ...
        """
        out: List[pd.DataFrame] = []
        for rep in self.fetch_report(symbol, limit):
            md = self._strip_frontmatter(rep.get("content", ""))
            out.extend(self._md_tables(md))
        return out

    @staticmethod
    def _strip_frontmatter(md: str) -> str:
        if md.startswith("---"):
            end = md.find("\n---", 3)
            if end != -1:
                return md[end + 4:].strip()
        return md

    @staticmethod
    def _md_tables(md: str) -> List[pd.DataFrame]:
        out: List[pd.DataFrame] = []
        for block in re.split(r"\n\s*\n", md):
            lines = [ln for ln in block.splitlines() if ln.strip().startswith("|")]
            if len(lines) < 2:
                continue
            rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
            header, body = rows[0], rows[2:]  # 第 2 行是 |---|---| 分隔行
            if not body:
                continue
            out.append(pd.DataFrame(body, columns=header))
        return out
