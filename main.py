from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

import main
from clerk import Clerk
from item import FourPackFactory, Item, SingleItemFactory, SixPackFactory
from product_db import ProductDb

app = FastAPI()

clerk: Clerk = Clerk()
oif: SingleItemFactory = SingleItemFactory()
tif: FourPackFactory = FourPackFactory()
sif: SixPackFactory = SixPackFactory()
count: int = 0


@app.get("/add_item/{item_name}", response_class=HTMLResponse)
async def add_item(item_name: str, action: int = 1) -> RedirectResponse:
    main.count += 1
    item: Item
    if action == 1:
        item = main.oif.create_product(item_name)
        main.clerk.add_item(item)
        print(item_name + " 1")
    elif action == 4:
        item = main.tif.create_product(item_name)
        main.clerk.add_item(item)
        print(item_name + " 4")
    elif action == 6:
        item = main.sif.create_product(item_name)
        print(item.amount)
        main.clerk.add_item(item)
        print(item_name + " 6")
    else:
        print("Fuck")
    response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
    return response


@app.get("/ClerkPage", response_class=HTMLResponse)
async def process_clerk() -> RedirectResponse:
    response = RedirectResponse(url="/")
    main.clerk.close_cashier()
    return response


@app.get("/ManagerPage", response_class=HTMLResponse)
async def process_manager() -> RedirectResponse:
    response = RedirectResponse(url="/")
    main.count = 10
    return response


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

    body += '<a href = "/ClerkPage">End of receipt</a>\n'
    body += '<a href = "/ManagerPage">Generate report X</a>'
    body += "<ul>"
    for item in main.clerk.get_customer_items():
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
    body += "<p>" + "Current price sum: " + str(main.clerk.sum_of_prices()) + "</p>"
    body += "</body>"

    return head + body + end
