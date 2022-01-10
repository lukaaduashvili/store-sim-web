from contextvars import ContextVar

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND, HTTP_404_NOT_FOUND

import main
from clerk import Clerk
from item import FourPackFactory, Item, SingleItemFactory, SixPackFactory
from manager import Manager
from product_db import ProductDb

app = FastAPI()
clerk: ContextVar[Clerk] = ContextVar("clk")
clerk.set(Clerk())
manager: ContextVar[Manager] = ContextVar("mng")
manager.set(Manager())
oif: SingleItemFactory = SingleItemFactory()
tif: FourPackFactory = FourPackFactory()
sif: SixPackFactory = SixPackFactory()
app.add_middleware(SessionMiddleware, secret_key="clerk")


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    db: ProductDb = ProductDb()
    head: str = """<html>
        <head>
            <title>Some HTML in here</title>
        </head>"""
    end: str = """</html>"""
    body: str = """
    <body>
    """
    cnt: int = 0
    for row in db.get_item_list():
        name: str = row[0]
        body += '<form method = "get" action = "/add_item/' + name + '">\n'
        cnt += 1
        body += (
            "<button type = 'submit' name = 'action' value = '1'>"
            + "Name: "
            + name
            + " Price: "
            + str(row[1])
            + " Count: 1"
            + " </button>\n"
        )
        body += (
            "<button type = 'submit' name = 'action' value = '4'>"
            + "Name: "
            + name
            + " Price: "
            + str(row[1])
            + " Count: 4"
            + " </button>\n"
        )
        body += (
            "<button type = 'submit' name = 'action' value = '6'>"
            + "Name: "
            + name
            + " Price: "
            + str(row[1])
            + " Count: 6"
            + " </button>\n"
        )
        body += "</form> \n"

    body += '<a href = "/ClerkPage">Process new client</a>\n'
    body += '<a href = "/ManagerPage">Generate report X</a>'
    body += "<ul>"
    for item in clerk.get().get_customer_items():
        body += (
            "<li>"
            + "Name: "
            + item.name
            + " Price: "
            + str(item.price * item.amount)
            + " Amount: "
            + str(item.amount)
            + "</li>"
        )

    body += "</ul>"
    body += "<p>" + "Current price sum: " + str(clerk.get().sum_of_prices()) + "</p>"
    body += "</body>"

    return head + body + end


@main.app.get("/add_item/{item_name}", response_class=HTMLResponse)
async def add_item(item_name: str, action: int = 1) -> RedirectResponse:
    item: Item
    if action == 1:
        item = main.oif.create_product(item_name)
        clerk.get().add_item(item, manager.get())
    elif action == 4:
        item = main.tif.create_product(item_name)
        clerk.get().add_item(item, manager.get())
    elif action == 6:
        item = main.sif.create_product(item_name)
        clerk.get().add_item(item, manager.get())
    else:
        response = RedirectResponse(url="/", status_code=HTTP_404_NOT_FOUND)
        return response
    response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
    return response


@main.app.get("/ClerkPage", response_class=HTMLResponse)
async def process_clerk() -> str:
    head: str = """<html>
           <head>
               <title>Some HTML in here</title>
           </head>"""
    end: str = """</html>"""
    body: str = """
       <body>
       """

    body += "<ul>"
    for item in clerk.get().get_customer_items():
        body += (
            "<li>"
            + "Name: "
            + item.name
            + " Price: "
            + str(item.price * item.amount)
            + " Amount: "
            + str(item.amount)
            + "</li>"
        )
    body += "</ul>"
    clerk.get().close_cashier()
    body += "<a href = '/'>Pay with card</a>"
    body += "<a href = '/'>Pay with cash</a>"
    return head + body + end


@main.app.get("/ManagerPage", response_class=HTMLResponse)
async def process_manager() -> str:
    head: str = """<html>
            <head>
                <title>Some HTML in here</title>
            </head>"""
    end: str = """</html>"""
    body: str = """
        <body>
        """
    tot_rev: str = str(manager.get().get_total_revenue())
    body += "<ul>"
    clerk.get().close_cashier()
    for pair in manager.get().generate_x_report():
        body += "<li>Name: " + pair[0]
        body += " Count: " + str(pair[1]) + "</li>"
    body += "</ul>"
    body += "<p>Total Revenue: " + tot_rev + "$</p>"
    body += "<a href = />Process new client</a>"
    body += "<body>"
    return head + body + end
