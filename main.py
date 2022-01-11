from contextvars import ContextVar
from typing import List

from fastapi import FastAPI
from starlette import status
from starlette.responses import Response

from clerk import Clerk
from item import FourPackFactory, Item, SingleItemFactory, SixPackFactory
from manager import Manager
from product_db import ProductDb
from report_x import ReportX

DB_ADDRESS: str = "products"

app = FastAPI()
manager: ContextVar[Manager] = ContextVar("mng")
manager.set(Manager())
db: ProductDb = ProductDb()
db.set_db_address(DB_ADDRESS)
clerk: Clerk = Clerk()


@app.put("/add_item/{item_name, item_price, item_amount}", status_code=200)
async def add_item(
    item_name: str, item_price: float, item_amount: int, response: Response
) -> str:
    if item_price > 0:
        db.add_item(item_name, item_price, item_amount)
        response.status_code = status.HTTP_201_CREATED
        return "Item added"
    else:
        response.status_code = status.HTTP_206_PARTIAL_CONTENT
        return "Item cant have negative price"


@app.post("/open_receipt", status_code=200)
async def open_client_receipt(response: Response) -> str:
    res: bool = clerk.begin_serving_client()
    if res:
        response.status_code = status.HTTP_200_OK
        return "Clerk started serving successfully"
    response.status_code = status.HTTP_400_BAD_REQUEST
    return "Clerk is busy close previous receipt"


@app.post("/add_item/{item_name, item_amount}", status_code=200)
async def add_client_item(item_name: str, item_amount: int, response: Response) -> str:
    if db.contains_item(item_name, item_amount):
        item: Item = Item()
        item.name = item_name
        item.amount = item_amount
        item.price = db.get_item_price(item.name, item.amount)
        res: bool = clerk.add_item(item, manager.get())
        if res:
            response.status_code = status.HTTP_200_OK
            return "Item added successfully"

        response.status_code = status.HTTP_400_BAD_REQUEST
        return "No client to serve, please open cash register"
    else:
        return "Store doesnt sell " + item_name + " in packs of" + str(item_amount)


@app.get("/get_current_receipt", status_code=200)
async def get_current_receipt() -> tuple[List[Item], float]:
    return clerk.receipt.get_info()


@app.post("/pay", status_code=200)
async def client_pay(response: Response) -> str:
    res: bool = clerk.close_cashier(manager.get())
    if res:
        response.status_code = status.HTTP_200_OK
        return "Client paid closing current receipt"
    response.status_code = status.HTTP_400_BAD_REQUEST
    return "Receipt is not open client can not pay"


@app.post("/report_x", status_code=200)
async def report_x() -> str:
    manager.get().generate_x_report()
    return "Report Successfully generated"


@app.get("/get_report", status_code=200)
async def get_latest_report() -> ReportX:
    return db.get_last_report()
