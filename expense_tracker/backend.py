from fastapi import FastAPI
from add_data import add_expense,delete_expense,show_expense,show_from_to
from connect_data import session,Expense,ExpenseCategory
import json
from pydantic import BaseModel

app=FastAPI()

from pydantic import BaseModel

class ExpenseData(BaseModel):
    date:str
    exp_name:str
    amount:float

class DelData(BaseModel):
    date:str
    exp_name:str

class DateRange(BaseModel):
    from_date:str
    to_date:str

class SingleDate(BaseModel):
    date:str

@app.post("/expense/enter_expense")
def enter_expense(data:ExpenseData):
    return add_expense(session=session,date=data.date,exp=data.exp_name,amount=data.amount)

@app.delete("/expense/delete")
def delete_exp(data:DelData):
    result=delete_expense(session=session,date=data.date,exp=data.exp_name)
    return {"success":result}

@app.post("/expense/show_expenses")
def show_exp(data:SingleDate):
    return show_expense(session,data.date)
    
@app.post("/expense/from_to_expense")
def from_to(data:DateRange):
    return show_from_to(session,data.from_date,data.to_date)


