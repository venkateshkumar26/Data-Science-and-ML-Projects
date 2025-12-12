import streamlit as st
import datetime
import requests
import pandas as pd

date = datetime.date.today()

st.title("Expense Tracker")

st.header("Add Expense")

chosen_date_add = st.date_input("Select date", value=date, key="add_date")
chosen_date_add_str = chosen_date_add.strftime("%Y-%m-%d")

exp_category_add = st.text_input("Enter the expense category:", key="add_cat").lower()
amount_add = st.number_input("Enter the amount:", min_value=0.0, step=0.5, key="add_amt")

if st.button("Submit Expense"):
    payload = {
        "date": chosen_date_add_str,
        "exp_name": exp_category_add,
        "amount": amount_add
    }

    try:
        resp = requests.post("http://127.0.0.1:8000/expense/enter_expense", json=payload)
        if resp.status_code == 200:
            st.success(f"Added {exp_category_add} on {chosen_date_add_str}")
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")


st.header("Delete Expense")

chosen_date_del = st.date_input("Select date to delete", value=date, key="del_date")
chosen_date_del_str = chosen_date_del.strftime("%Y-%m-%d")

exp_category_del = st.text_input("Enter expense category to delete:", key="del_cat").lower()

if st.button("Delete Expense"):
    payload = {
        "date": chosen_date_del_str,
        "exp_name": exp_category_del
    }

    try:
        resp = requests.delete("http://127.0.0.1:8000/expense/delete", json=payload)
        if resp.status_code == 200 and resp.json()["success"]:
            st.success(f"Deleted {exp_category_del} on {chosen_date_del_str}")
        else:
            st.error(f"Delete failed: {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")

st.header("Show Expenses")

from_date = st.date_input("From Date", value=date, key="show_from")
from_date_str = from_date.strftime("%Y-%m-%d")

to_date = st.date_input("To Date", value=date, key="show_to")
to_date_str = to_date.strftime("%Y-%m-%d")

URL_SINGLE = "http://127.0.0.1:8000/expense/show_expenses"
URL_RANGE = "http://127.0.0.1:8000/expense/from_to_expense"

if st.button("Show Range"):
    payload = {
        "from_date": from_date_str,
        "to_date": to_date_str
    }

    resp = requests.post(URL_RANGE, json=payload)
    data = resp.json()

    if not data:
        st.warning("No data found in the selected range.")
    else:
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        st.dataframe(df)

if st.button("Show Single Date"):
    payload = {"date": from_date_str}

    resp = requests.post(URL_SINGLE, json=payload)
    data = resp.json()

    if not data:
        st.warning("No expenses for this date.")
    else:
        st.dataframe(data)
