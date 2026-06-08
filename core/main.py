from typing import List

from database import Expense
from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schemas import ExpenseCreateSchema, ExpenseEditSchema, ExpenseResponseSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

app = FastAPI()
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db  # The session is handed over to the FastAPI route here
    finally:
        db.close()  # This runs automatically after the API response is sent


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/expenses", response_model=List[ExpenseResponseSchema])
async def retrieveExpensesList(q: str | None = Query(alias="search", default=None), db: Session = Depends(get_db)):
    query = db.query(Expense)
    if q:
        query = query.filter(Expense.description.ilike(f"%{q}%"))
    expenses = query.all()
    return expenses


@app.get("/expenses/{item_id}", response_model=ExpenseResponseSchema)
async def readExpense(item_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == item_id).one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="item not found.")
    return expense


@app.post("/expenses", response_model=ExpenseResponseSchema)
async def addExpense(item: ExpenseCreateSchema, db: Session = Depends(get_db)):
    expense_data = Expense(**item.model_dump())
    db.add(expense_data)
    db.commit()
    db.refresh(expense_data)
    return JSONResponse(content=jsonable_encoder(expense_data), status_code=status.HTTP_201_CREATED)


@app.put("/expenses/{item_id}", response_model=ExpenseResponseSchema)
async def changeExpense(item_id: int, item: ExpenseEditSchema, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == item_id).one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="item not found.")
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
            setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense


@app.delete("/names/{item_id}")
async def deleteItem(item_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == item_id).one_or_none()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="object not found."
        )
    db.delete(expense)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
