from connect_data import Expense,ExpenseCategory,session

def add_expense(session,date:str,exp:str,amount:float):
    try:
        category=session.query(ExpenseCategory).filter_by(exp_name=exp).first()
        if not category:
            category=ExpenseCategory(exp_name=exp)
            session.add(category)
            session.commit()
            session.refresh(category)
        expense=Expense(date=date,exp_id=category.exp_id,amount=amount)
        session.add(expense)
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def delete_expense(session, date: str, exp: str):
    try:
        print("DELETE DEBUG INPUTS:", date, exp)

        exp = exp.lower().strip()
        date = date.strip()

        category = session.query(ExpenseCategory).filter_by(exp_name=exp).first()
        print("CATEGORY FOUND:", category.exp_id if category else None)

        deleted = session.query(Expense).filter_by(
            date=date,
            exp_id=category.exp_id if category else None
        ).delete()

        print("DELETED COUNT:", deleted)

        session.commit()

        return deleted > 0


    except Exception as e:
        print("Error deleting expense:", e)
        return False

def show_expense(session, date: str):
    try:
        expenses = session.query(Expense).filter_by(date=date).all()

        result = []

        for exp in expenses:
            category = session.query(ExpenseCategory).filter_by(exp_id=exp.exp_id).first()

            result.append({
                "category": category.exp_name if category else "Unknown",
                "amount": exp.amount
            })

        return result

    except Exception as e:
        print("Error:", e)
        return []

def show_from_to(session, from_date: str, to_date: str):
    try:
        expenses = (
            session.query(Expense, ExpenseCategory)
            .join(ExpenseCategory, Expense.exp_id == ExpenseCategory.exp_id)
            .filter(Expense.date.between(from_date, to_date))
            .all()
        )

        result = []
        for exp, cat in expenses:
            result.append({
                "date": exp.date,
                "category": cat.exp_name,
                "amount": exp.amount
            })

        return result

    except Exception as e:
        print("Error:", e)
        return []


            


        
