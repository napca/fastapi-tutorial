from pydantic import BaseModel, Field
from typing import Optional
class ExpenseBaseSchema(BaseModel):
    amount: float = Field(gt=0, description="The cost of the expense, must be greater than zero")
    description: Optional[str] = Field(default=None, max_length=255, description="Optional details about the expense")
class ExpenseCreateSchema(ExpenseBaseSchema):
    pass
class ExpenseResponseSchema(ExpenseBaseSchema):
    id: int
class ExpenseEditSchema(ExpenseBaseSchema):
    amount: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = Field(default=None, max_length=255)
