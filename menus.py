from datetime import datetime
from expense import Expense, CATEGORIES
from data_store import save_expenses


DIVIDER = "-" * 75

class ReturnHome(Exception):
    pass

def get_input(prompt):
    """Ask for input. q quits the app, back (or r) returns to the home menu."""
    text = input(prompt).strip()
    if text.lower() == "q":
        print("Goodbye! Your expenses are saved.")
        raise SystemExit
    if text.lower() == "r":
        raise ReturnHome
    return text

def home_menu():
    print("\n" + DIVIDER)
    print("BUDGET BUDDY")
    print("Track your spending.")
    print("Free. Your data stays locally on this computer.")
    print("Adding an expense takes a few seconds.")
    print("\n" + DIVIDER)
    print("1. View your expenses")
    print("2. Add an expense")
    print("3. Delete an expense")
    print("4. Help")
    print("5. Quit")
    print(DIVIDER + "\n")

def add_expense(expenses):
    while True:
        print("\n" + DIVIDER)
        print("ADD AN EXPENSE")
        print("You will enter 3 things: amount, date, category.")
        print("Type r at any time to return home, or q to quit.")
        print(DIVIDER)

        amount = ask_amount()
        if amount is None:
            return
        date = ask_date()
        if date is None:
            return
        category = ask_category()
        if category is None:
            return

        expense = Expense(amount, date, category)
        expenses.append(expense)
        save_expenses(expenses)

        print("\n" + DIVIDER)
        print("Expense saved!")
        expense.print_details()
        print(DIVIDER + "\n")

        print("1. Add another expense")
        print("2. Return home")
        if input("Type a number: ").strip() != "1":
            return

def ask_date():
    while True:
        text = input("Step 2 of 3 - Date as MM/DD/YYYY (press Enter for today): ").strip()
        if text.lower() == "r":
            return None
        if text == "":
            return datetime.now().strftime("%m/%d/%Y")
        try:
            return datetime.strptime(text, "%m/%d/%Y").strftime("%m/%d/%Y")
        except ValueError:
            print("Please enter a date like 11/06/2026, or press Enter for today.")

def ask_category():
    print("Step 3 of 3 - Category:")
    for number, name in enumerate(CATEGORIES, start=1):
        print(f"  {number}. {name}")
    while True:
        text = input("Type a number: ").strip()
        if text.lower() == "r":
            return None
        if text.isdigit() and 1 <= int(text) <= len(CATEGORIES):
            return CATEGORIES[int(text) - 1]
        print(f"Please type a number from 1 to {len(CATEGORIES)}.")

def ask_amount():
    while True:
        text = input("Step 1 of 3 - Amount (example: 12.50): ").strip()
        if text.lower() == "r":
            return None
        try:
            amount = round(float(text), 2)
        except ValueError:
            amount = 0
        if 0 < amount < 1000000:
            return amount
        print("Please enter a positive number, like 12.50.")

def print_table(expenses):
    """Sort the expenses by date and print them as a numbered table."""
    expenses.sort(key=lambda e: datetime.strptime(e.date, "%m/%d/%Y"))
    print(f"{'#':<4}{'Date':<13}{'Category':<17}{'Amount':>10}")
    for number, expense in enumerate(expenses, start=1):
        amount_text = f"${expense.amount:.2f}"
        print(f"{number:<4}{expense.date:<13}{expense.category:<17}{amount_text:>10}")
        
def view_expenses(expenses):
    print("\n" + DIVIDER)
    print("YOUR EXPENSES")
    print(DIVIDER)
    if not expenses:
        print("You have no expenses yet.")
        print("Choose 1 below to add one.")
    else:
        print_table(expenses)
        total = round(sum(e.amount for e in expenses), 2)
        word = "expense" if len(expenses) == 1 else "expenses"
        print(DIVIDER)
        print(f"Total: ${total:.2f} ({len(expenses)} {word})")
    print(DIVIDER + "\n")
    print("1. Add an expense")
    print("2. Delete an expense")
    print("3. Return home")

    while True:
        choice = get_input("Type a number: ")
        if choice in ("1", "2", "3"):
            break
        print("Please type 1, 2 or 3.")

    if choice == "1":
        add_expense(expenses)
    elif choice == "2":
        delete_expense(expenses)

def delete_expense(expenses):
    while True:
        print("\n" + DIVIDER)
        print("DELETE AN EXPENSE")
        print(DIVIDER)
        if not expenses:
            print("You have no expenses to delete.")
            print(DIVIDER)
            input("Press Enter to return home.")
            return

        print_table(expenses)
        print(DIVIDER)
        print("Type r at any time to return home, or q to quit.")

        # Step 1: choose which expense
        while True:
            text = get_input("Type the number of the expense to delete: ")
            if text.isdigit() and 1 <= int(text) <= len(expenses):
                break
            print(f"Please type a number from 1 to {len(expenses)}.")
        index = int(text) - 1

        # Step 2: confirm
        expense = expenses[index]
        print("\n" + DIVIDER)
        print("You chose:")
        expense.print_details()
        print(DIVIDER)
        print("Changed your mind later? You can undo right after deleting.")
        while True:
            answer = get_input("Delete this expense? (y/n): ").lower()
            if answer in ("y", "n"):
                break
            print("Please type y or n.")

        if answer == "n":
            print("Nothing was deleted.")
            print(DIVIDER)
            input("Press Enter to return home.")
            return

        # Step 3: delete it, then offer undo
        deleted = expenses.pop(index)
        save_expenses(expenses)
        print("\n" + DIVIDER)
        print("Expense deleted.")
        print(DIVIDER)
        print("1. Undo delete")
        print("2. Delete another expense")
        print("3. Return home")
        while True:
            option = get_input("Type a number: ")
            if option in ("1", "2", "3"):
                break
            print("Please type 1, 2 or 3.")

        if option == "1":
            expenses.append(deleted)
            save_expenses(expenses)
            print("\n" + DIVIDER)
            print("Expense restored.")
            deleted.print_details()
            print(DIVIDER)
            input("Press Enter to return home.")
            return
        elif option == "3":
            return
        
def help_menu():
    print("\n" + DIVIDER)
    print("HELP")
    print(DIVIDER)
    print("To add an expense:")
    print("  1. From the home menu, type 2.")
    print("  2. Enter the amount, the date and the category.")
    print()
    print("To view your expenses:")
    print("  1. From the home menu, type 1.")
    print("  2. You will see all your expenses and the total.")
    print()
    print("To delete an expense:")
    print("  1. From the home menu, type 3.")
    print("  2. Type the number of the expense, then y to confirm.")
    print("  3. Changed your mind? Choose Undo right after deleting.")
    print(DIVIDER)
    print("Tips:")
    print("  Type r at any time to return home.")
    print("  Type q at any time to quit.")
    print("  Your expenses are saved automatically.")
    print(DIVIDER)
    input("Press Enter to return home.")
