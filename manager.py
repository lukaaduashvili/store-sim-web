from typing import List

from product_db import ProductDb
from receipt import ManagerReceipt


class Manager:
    # def update(self, subject: Subject) -> List[tuple[str, int]]:
    #     items: List[tuple[str, int]] = subject.m_receipt.get_all_items()
    #     subject.m_receipt = ManagerReceipt()
    #     return items

    def __init__(self) -> None:
        self.receipt: ManagerReceipt = ManagerReceipt()
        self.db: ProductDb = ProductDb()

    def backup_report(self, items: List[tuple[str, int]], total_rev: float) -> None:
        self.db.add_report(items, total_rev)

    def generate_x_report(self) -> List[tuple[str, int]]:
        items: List[tuple[str, int]] = self.receipt.get_all_items()
        self.backup_report(items, self.get_total_revenue())
        self.receipt = ManagerReceipt()
        return items

    def get_total_revenue(self) -> float:
        return self.receipt.get_final_revenue()
