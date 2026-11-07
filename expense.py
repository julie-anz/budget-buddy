CATEGORIES = ["Food", "Housing", "Transportation", "Other"]

class Expense:
    def __init__(self, amount, date, category):
        self.amount = amount
        self.date = date
        self.category = category

    def to_dict(self):
        return {
            "amount": self.amount,
            "date": self.date,
            "category": self.category
        }

    def print_details(self):
        print(f"  Amount:   ${self.amount:.2f}")
        print(f"  Date:      {self.date}")
        print(f"  Category:  {self.category}")