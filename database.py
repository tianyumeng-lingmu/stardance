# 群星之舞 (Star Dance) - 内置 SQLite 数据库

import sqlite3
import os
from typing import Optional


class StarDatabase:
    """
    群星之舞的内置 SQLite 数据库。
    每个 .star 程序启动时自动创建一个同名的 .db 文件。
    """

    def __init__(self, db_path: str = None):
        # 默认在程序运行目录创建 star_dance.db
        if db_path is None:
            db_path = os.path.join(os.getcwd(), 'star_dance.db')
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self._connect()

    def _connect(self):
        """连接到 SQLite 数据库（自动创建）"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        # 启用 WAL 模式以提升并发性能
        self.execute("PRAGMA journal_mode=WAL")
        # 启用外键约束
        self.execute("PRAGMA foreign_keys=ON")

    def execute(self, sql: str, params: tuple = ()) -> dict:
        """
        执行 SQL 语句（INSERT / UPDATE / DELETE / CREATE 等）
        返回: {"success": True, "affected_rows": N}
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            self.connection.commit()
            return {
                "success": True,
                "affected_rows": cursor.rowcount,
                "last_row_id": cursor.lastrowid,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def query(self, sql: str, params: tuple = ()) -> dict:
        """
        执行 SQL 查询（SELECT）
        返回: {"success": True, "columns": [...], "rows": [[...], ...]}
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = [list(row) for row in cursor.fetchall()]
            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        result = self.query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return result["success"] and len(result["rows"]) > 0

    def create_table(self, table_name: str, columns: str) -> dict:
        """创建表: CREATE TABLE IF NOT EXISTS name (columns)"""
        return self.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

    def drop_table(self, table_name: str) -> dict:
        """删除表"""
        return self.execute(f"DROP TABLE IF EXISTS {table_name}")

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def __repr__(self):
        return f"StarDatabase({self.db_path})"
