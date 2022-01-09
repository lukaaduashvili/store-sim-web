from typing import List

from item import Item


class Receipt:
    def __init__(self) -> None:
        self.items: List[Item] = []

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def get_price(self) -> float:
        res: float = 0
        for item in self.items:
            res += item.price * item.amount
        return res

    def get_items(self) -> List[Item]:
        return self.items
