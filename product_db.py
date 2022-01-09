import sqlite3
from typing import List

from singleton import Singleton


class ProductDb(metaclass=Singleton):
    con = sqlite3.connect("products")
    cur = con.cursor()
    cur.execute("DROP TABLE prices")
    cur.execute(
        """CREATE TABLE IF NOT EXISTS prices
                   (name text, price real, UNIQUE(name))"""
    )
    cur.execute("INSERT OR IGNORE INTO prices VALUES ('Apple', 1.25)")
    cur.execute("INSERT OR IGNORE INTO prices VALUES ('Banana', 2.5)")
    cur.execute("INSERT OR IGNORE INTO prices VALUES ('Cucumber', 1.25)")
    cur.execute("INSERT OR IGNORE INTO prices VALUES ('Beer', 2.5)")
    cur.execute("INSERT OR IGNORE INTO prices VALUES ('Bread', 1.5)")
    cur.execute("INSERT OR IGNORE INTO prices VALUES ('Milk', 1.5)")
    con.commit()

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
