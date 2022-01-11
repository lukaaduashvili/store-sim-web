import datetime
import sqlite3
from typing import Any, List

from report_x import ReportItem, ReportX
from singleton import Singleton


class ProductDb(metaclass=Singleton):
    DB_ADDRESS: str = "products"

    def __init__(self) -> None:
        self.con: Any = None
        self.cur: Any = None

    def set_db_address(self, db_address: str) -> None:
        self.con = sqlite3.connect(db_address)
        self.cur = self.con.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS prices
                       (name text, price real, pack_size int)"""
        )
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS reports
                            (rep_time date, revenue float, rec_cnt int)"""
        )

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS report_items
                            (rep_id int, item_name text, amount real)"""
        )

        self.con.commit()

    def contains_item(self, item_name: str, item_amount: int) -> bool:
        self.cur.execute(
            "SELECT COUNT(*) from prices WHERE name LIKE ? AND pack_size = ?",
            (item_name, item_amount),
        )
        curr_id: int = self.cur.fetchall()[0][0]
        return curr_id > 0

    def add_report(
        self, items: List[tuple[str, int]], total_rev: float, cnt: int
    ) -> None:
        self.cur.execute(
            "INSERT OR IGNORE INTO reports VALUES(?, ?, ?)",
            (datetime.datetime.now(), total_rev, cnt),
        )
        self.con.commit()
        res = self.cur.execute("SELECT COUNT(*) FROM reports")
        rep_id: int = res.fetchall()[0][0]
        for row in items:
            self.cur.execute(
                "INSERT OR IGNORE INTO report_items VALUES(?, ?, ?)",
                (rep_id, row[0], row[1]),
            )
        self.con.commit()

    def add_item(self, p_name: str, p_price: float, p_amount: int) -> None:
        self.cur.execute(
            "INSERT OR IGNORE INTO prices values (?, ?, ?)", (p_name, p_price, p_amount)
        )
        self.con.commit()

    def get_item_price(self, p_name: str, p_amount: int) -> float:
        self.cur.execute(
            "SELECT price from prices WHERE name LIKE ? AND pack_size = ?",
            (p_name, p_amount),
        )
        row = self.cur.fetchall()
        return float(row[0][0])

    def get_last_report(self) -> ReportX:
        self.cur.execute(
            "SELECT COUNT(*) from reports",
        )
        r_id: int = self.cur.fetchall()[0][0]
        query = self.cur.execute("SELECT * from reports WHERE rowid = ?", (r_id,))
        res1 = query.fetchall()

        query = self.cur.execute("SELECT * from report_items WHERE rep_id = ?", (r_id,))
        res2 = query.fetchall()
        temp_list: List[ReportItem] = []
        for i in range(len(res2)):
            temp_list.append(ReportItem(res2[i][1], res2[i][2]))
        report: ReportX = ReportX(res1[0][0], res1[0][1], res1[0][2], temp_list)
        return report
