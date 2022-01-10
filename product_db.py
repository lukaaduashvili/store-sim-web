import datetime
import sqlite3
from typing import List

from singleton import Singleton


class ProductDb(metaclass=Singleton):
    def __init__(self) -> None:
        self.con = sqlite3.connect("products")
        self.cur = self.con.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS prices
                       (name text, price real, UNIQUE(name))"""
        )
        self.cur.execute("INSERT OR IGNORE INTO prices VALUES ('Apple', 1.25)")
        self.cur.execute("INSERT OR IGNORE INTO prices VALUES ('Banana', 2.5)")
        self.cur.execute("INSERT OR IGNORE INTO prices VALUES ('Cucumber', 1.25)")
        self.cur.execute("INSERT OR IGNORE INTO prices VALUES ('Beer', 2.5)")
        self.cur.execute("INSERT OR IGNORE INTO prices VALUES ('Bread', 1.5)")
        self.cur.execute("INSERT OR IGNORE INTO prices VALUES ('Milk', 1.5)")

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS reports
                            (rep_time date, revenue float)"""
        )

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS report_items
                            (rep_id int, item_name text, amount real)"""
        )

        self.con.commit()

    def add_report(self, items: List[tuple[str, int]], total_rev: float) -> None:
        self.cur.execute(
            "INSERT OR IGNORE INTO reports VALUES(?, ?)",
            (datetime.datetime.now(), total_rev),
        )
        self.con.commit()
        res = self.cur.execute("SELECT COUNT(*) FROM reports")
        rep_id: int = res.fetchall()[0][0]
        print(rep_id)
        for row in items:
            self.cur.execute(
                "INSERT OR IGNORE INTO report_items VALUES(?, ?, ?)",
                (rep_id, row[0], row[1]),
            )
        self.con.commit()

    def get_item_list(self) -> List[tuple[str, float]]:
        self.cur.execute("SELECT * FROM prices ORDER BY price")
        res = self.cur.fetchall()
        return res

    def add_item(self, p_name: str, p_price: float) -> None:
        self.cur.execute(
            "INSERT OR IGNORE INTO prices values (?, ?)", (p_name, p_price)
        )
        self.con.commit()

    def get_item_price(self, p_name: str) -> float:
        self.cur.execute("SELECT price from prices WHERE name like ?", (p_name,))
        row = self.cur.fetchall()
        return float(row[0][0])
