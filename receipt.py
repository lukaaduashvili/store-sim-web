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

    def get_info(self) -> tuple[List[Item], float]:
        return self.items, self.get_price()


class ManagerReceipt:
    def __init__(self) -> None:
        self.all_items: dict[str, int] = dict()
        self.total_sum: float = 0
        self.num_receipts: int = 0

    def add_item(self, item: Item) -> None:
        if item.name in self.all_items:
            self.all_items[item.name] = self.all_items[item.name] + item.amount
        else:
            self.all_items.update({item.name: item.amount})
        self.total_sum += item.price * item.amount

    def get_all_items(self) -> List[tuple[str, int]]:
        item_names: List[str] = []
        item_amounts: List[int] = []
        for item in self.all_items:
            amount: int = self.all_items[item]
            item_names.append(item)
            item_amounts.append(amount)
        items: List[tuple[str, int]] = list(zip(item_names, item_amounts))
        return items

    def get_final_revenue(self) -> float:
        return self.total_sum

    def add_count(self) -> None:
        self.num_receipts += 1

    def get_receipts(self) -> int:
        return self.num_receipts
