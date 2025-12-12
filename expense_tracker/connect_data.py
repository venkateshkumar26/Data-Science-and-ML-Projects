from sqlalchemy import create_engine,Column,Integer,Float,Text,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
import os


Base=declarative_base()

class ExpenseCategory(Base):
    __tablename__="expense_category"
    
    exp_id=Column(Integer,autoincrement=True,primary_key=True)
    exp_name=Column(String(100),unique=True,nullable=False)


class Expense(Base):
    __tablename__="expense"

    id=Column(Integer,autoincrement=True,primary_key=True)
    date=Column(String,nullable=False)
    exp_id=Column(Integer,ForeignKey("expense_category.exp_id"))
    amount=Column(Float,nullable=False)
    category=relationship("ExpenseCategory")



engine=create_engine("sqlite:///expenses.db")
Base.metadata.create_all(engine)
Session=sessionmaker(autoflush=False,autocommit=False,bind=engine)
session=Session()
