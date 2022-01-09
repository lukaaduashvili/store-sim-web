from typing import List

from item import Item
from observer_interfaces import Observer, Subject
from receipt import Receipt


class Clerk(Subject):
    def __init__(self) -> None:
        self.observers: List[Observer] = []
        self.receipt = Receipt()

    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)

    def add_item(self, item: Item) -> None:
        self.receipt.add_item(item)

    def sum_of_prices(self) -> float:
        return self.receipt.get_price()

    def print_x_report(self) -> None:
        pass

    def close_cashier(self) -> None:
        self.receipt = Receipt()

    def get_customer_items(self) -> List[Item]:
        return self.receipt.get_items()
