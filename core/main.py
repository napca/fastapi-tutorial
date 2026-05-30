import random

from fastapi import Body, FastAPI, HTTPException, Response, status

app = FastAPI()
itemsList = {1: {"id": 1, "description": "", "amount": 20.0}}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/expenses")
async def retrieveExpensesList():
    return itemsList


@app.get("/expenses/{item_id}")
async def readExpense(item_id: int):
    if item_id not in itemsList:
        raise HTTPException(status_code=404, detail="item not found.")
    return itemsList[item_id]


@app.post(("/expenses"))
async def addExpense(amount: float = Body(), description: str | None = Body(None)):
    id = 1
    while id in itemsList:
        id = random.randint(1, 1000)
    itemsList[id] = {"id": id, "description": description, "amount": amount}
    return itemsList[id]


@app.put("/expenses/{item_id}")
async def changeExpense(
    item_id: int, amount: float = Body(), description: str | None = Body(None)
):
    if item_id not in itemsList:
        raise HTTPException(status_code=404, detail="item not found.")
    itemsList[item_id]["description"] = description
    itemsList[item_id]["amount"] = amount
    return itemsList[item_id]


@app.delete("/names/{item_id}")
async def deleteItem(item_id: int):
    if item_id not in itemsList:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="object not found."
        )
    itemsList.pop(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
