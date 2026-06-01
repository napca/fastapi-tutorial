import random
from typing import List

from fastapi import Body, FastAPI, HTTPException, Query, Response, status
from fastapi.responses import JSONResponse
from schemas import ExpenseCreateSchema, ExpenseEditSchema, ExpenseResponseSchema

app = FastAPI()
itemsList = {1: {"id": 1, "description": "hello there", "amount": 20.0}}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/expenses", response_model=List[ExpenseResponseSchema])
async def retrieveExpensesList(q: str | None = Query(alias="search", default=None)):
    if q:
        return [item for item in itemsList.values() if item["description"].find(q) != -1]
    return itemsList.values()


@app.get("/expenses/{item_id}", response_model=ExpenseResponseSchema)
async def readExpense(item_id: int):
    if item_id not in itemsList:
        raise HTTPException(status_code=404, detail="item not found.")
    return itemsList[item_id]


@app.post("/expenses", response_model=ExpenseResponseSchema)
async def addExpense(item: ExpenseCreateSchema):
    id = 1
    expense_data = item.model_dump()
    while id in itemsList:
        id = random.randint(1, 1000)
        expense_data["id"] = id
    itemsList[id] = expense_data
    return JSONResponse(content=itemsList[id], status_code=status.HTTP_201_CREATED)


@app.put("/expenses/{item_id}", response_model=ExpenseResponseSchema)
async def changeExpense(
        item_id: int, item:ExpenseEditSchema
):
    if item_id not in itemsList:
        raise HTTPException(status_code=404, detail="item not found.")
    update_data = item.model_dump(exclude_unset=True)
    itemsList[item_id].update(update_data)
    return itemsList[item_id]


@app.delete("/names/{item_id}")
async def deleteItem(item_id: int):
    if item_id not in itemsList:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="object not found."
        )
    itemsList.pop(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
