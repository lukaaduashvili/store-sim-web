from typing import List

from item import Item
from manager import Manager
from receipt import ManagerReceipt, Receipt


class Clerk:
    def __init__(self) -> None:
        self.receipt: Receipt = Receipt()
        self.m_receipt: ManagerReceipt = ManagerReceipt()

    def add_item(self, item: Item, manager: Manager) -> None:
        self.receipt.add_item(item)
        manager.receipt.add_item(item)

    def sum_of_prices(self) -> float:
        return self.receipt.get_price()

    def close_cashier(self, manager: Manager) -> None:
        manager.receipt.add_count()
        self.receipt = Receipt()

    def get_customer_items(self) -> List[Item]:
        return self.receipt.get_items()
