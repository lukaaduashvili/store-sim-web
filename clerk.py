from typing import List

from item import Item
from manager import Manager
from receipt import ManagerReceipt, Receipt


class Clerk:
    def __init__(self) -> None:
        self.receipt: Receipt = Receipt()
        self.m_receipt: ManagerReceipt = ManagerReceipt()
        self.ready_to_serve: bool = False

    def begin_serving_client(self) -> bool:
        if self.ready_to_serve:
            return False
        self.ready_to_serve = True
        return True

    def add_item(self, item: Item, manager: Manager) -> bool:
        if self.ready_to_serve:
            self.receipt.add_item(item)
            manager.receipt.add_item(item)
            return True
        return False

    def sum_of_prices(self) -> float:
        return self.receipt.get_price()

    def close_cashier(self, manager: Manager) -> bool:
        if self.ready_to_serve:
            manager.receipt.add_count()
            self.receipt = Receipt()
            self.ready_to_serve = False
            return True
        return False

    def get_customer_items(self) -> List[Item]:
        return self.receipt.get_items()
