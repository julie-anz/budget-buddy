
from data_store import load_expenses
from menus import *


def main():
    expenses = load_expenses()
    while True:
        try:
            home_menu()
            choice = get_input("Type a number (or q to quit): ")
            if choice == "5":
                print("Goodbye! Your expenses are saved.")
                break
            elif choice == "1":
                view_expenses(expenses)
            elif choice == "2":
                add_expense(expenses)
            elif choice == "3":
                delete_expense(expenses)
            elif choice == "4":
                help_menu()
            else:
                print("Please type a number from 1 to 5.")
        except ReturnHome:
            pass

if __name__ == "__main__":
    main()
