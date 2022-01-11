from typing import List


class ReportItem:
    def __init__(self, name: str, amount: int) -> None:
        self.name = name
        self.amount = amount


class ReportX:
    def __init__(
        self, date: str, revenue: float, num_receipts: int, items: List[ReportItem]
    ) -> None:
        self.date = date
        self.revenue = revenue
        self.num_receipts = num_receipts
        self.items = items
