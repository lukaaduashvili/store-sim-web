import sqlite3

from clerk import Clerk
from item import FourPackFactory, Item, SingleItemFactory, SixPackFactory
from manager import Manager
from product_db import ProductDb
from receipt import ManagerReceipt, Receipt
from report_x import ReportX

db: ProductDb = ProductDb()
db.set_db_address("test")


def test_add_to_db() -> None:
    db.add_item("Cheese", 1.98, 2)
    assert db.get_item_price("Cheese", 2) == 1.98


def test_contains() -> None:
    assert db.contains_item("Cheese", 2)


def test_item() -> None:
    item: Item = Item()
    item.name = "Dog"
    item.amount = 1
    item.price = 3.99
    assert item.name == "Dog"
    assert item.amount == 1
    assert item.price == 3.99


def test_one_item_factory() -> None:
    one_factory: SingleItemFactory = SingleItemFactory()
    item: Item = one_factory.create_product("Apple", 1.25)
    assert item.name == "Apple"
    assert item.price == 1.25
    assert item.amount == 1


def test_four_item_factory() -> None:
    four_factory: FourPackFactory = FourPackFactory()
    item: Item = four_factory.create_product("Apple", 1.25)
    assert item.name == "Apple"
    assert item.price == 1.25
    assert item.amount == 4


def test_six_item_factory() -> None:
    six_factory: SixPackFactory = SixPackFactory()
    item: Item = six_factory.create_product("Apple", 1.25)
    assert item.name == "Apple"
    assert item.price == 1.25
    assert item.amount == 6


def test_receipt() -> None:
    item1: Item = Item()
    item1.name = "Apple"
    item1.price = 1.99
    item1.amount = 1
    item6: Item = Item()
    item6.name = "Apple"
    item6.price = 1.99
    item6.amount = 6
    receipt: Receipt = Receipt()
    receipt.add_item(item1)
    receipt.add_item(item6)
    assert len(receipt.get_items()) == 2
    assert receipt.get_items()[0].amount == 1
    assert receipt.get_items()[1].amount == 6
    assert (
        receipt.get_price() == item1.amount * item1.price + item6.amount * item6.price
    )


def test_manager_receipt() -> None:
    item1: Item = Item()
    item1.name = "Apple"
    item1.price = 1.99
    item1.amount = 1
    item6: Item = Item()
    item6.name = "Apple"
    item6.price = 1.99
    item6.amount = 6
    receipt: ManagerReceipt = ManagerReceipt()
    receipt.add_item(item1)
    receipt.add_item(item6)
    receipt.add_count()
    receipt.add_item(item1)
    receipt.add_count()
    assert (
        receipt.get_final_revenue()
        == 2 * item1.amount * item1.price + item6.amount * item6.price
    )
    assert receipt.get_receipts() == 2
    assert receipt.get_all_items()[0][0] == "Apple"
    assert receipt.get_all_items()[0][1] == 8


def test_clerk_and_manager() -> None:
    item1: Item = Item()
    item1.name = "Apple"
    item1.price = 1.99
    item1.amount = 1
    item4: Item = Item()
    item4.name = "Apple"
    item4.price = 1.99
    item4.amount = 4
    item6: Item = Item()
    item6.name = "Apple"
    item6.price = 1.99
    item6.amount = 6
    clerk: Clerk = Clerk()
    manager: Manager = Manager()
    clerk.begin_serving_client()
    clerk.add_item(item1, manager)
    clerk.add_item(item6, manager)
    assert clerk.get_customer_items()[0] == item1
    assert clerk.get_customer_items()[1] == item6
    assert (
        clerk.sum_of_prices() == item1.amount * item1.price + item6.amount * item6.price
    )
    clerk.close_cashier(manager)
    assert (
        manager.get_total_revenue()
        == item1.amount * item1.price + item6.amount * item6.price
    )
    clerk.begin_serving_client()
    clerk.add_item(item4, manager)
    assert clerk.get_customer_items()[0] == item4
    assert (
        manager.get_total_revenue()
        == item1.amount * item1.price
        + item6.amount * item6.price
        + item4.amount * item4.price
    )
    clerk.close_cashier(manager)

    con = sqlite3.connect("test")
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) from reports")
    prev_id: int = cur.fetchall()[0][0]

    manager.generate_x_report()
    assert manager.get_total_revenue() == 0

    cur.execute("SELECT COUNT(*) from reports")
    curr_id: int = cur.fetchall()[0][0]
    assert curr_id - prev_id == 1


def test_latest_report() -> None:
    rep: ReportX = db.get_last_report()
    assert rep.num_receipts == 2
    assert rep.revenue == 21.89
