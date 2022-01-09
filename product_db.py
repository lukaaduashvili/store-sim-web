from singleton import Singleton


class ProductDb(metaclass=Singleton):
    def get_item_price(self, name: str) -> int:
        return -1
