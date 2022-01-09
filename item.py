from abc import abstractmethod
from dataclasses import dataclass

from product_db import ProductDb
from singleton import Singleton


@dataclass
class Item:
    amount: int = 0
    price: float = 0
    name: str = ""


class AbstractFactory(metaclass=Singleton):
    productDb = ProductDb()

    @abstractmethod
    def create_product(self, name: str) -> Item:
        pass


class SingleItemFactory(AbstractFactory):
    def create_product(self, name: str) -> Item:
        itm = Item()
        itm.amount = 1
        itm.price = self.productDb.get_item_price(name)
        itm.name = name
        return itm


class FourPackFactory(AbstractFactory):
    def create_product(self, name: str) -> Item:
        itm = Item()
        itm.amount = 4
        itm.price = self.productDb.get_item_price(name)
        itm.name = name
        return itm


class SixPackFactory(AbstractFactory):
    def create_product(self, name: str) -> Item:
        itm = Item()
        itm.amount = 6
        itm.price = self.productDb.get_item_price(name)
        itm.name = name
        return itm
