import os
import json
from expense import Expense

DATA_FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return [Expense(**expense_data) 
                for expense_data in json.load(file)]

def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump([expense.to_dict() 
                   for expense in expenses], file, indent=4)
