import csv
import shutil
from datetime import datetime
import matplotlib.pyplot as plt

EXPENSES_FILE = "expenses.csv"

def log_expense():
    """Log a daily expense."""
    name = input("Enter your name: ").strip()
    date = input("Enter the date (YYYY-MM-DD): ").strip()
    description = input("Enter a description of the expense: ").strip()
    amount = float(input("Enter the amount spent: "))
    category = input("Enter the category (e.g., groceries, utilities, entertainment): ").strip()

    with open(EXPENSES_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Write header if the file is empty
            writer.writerow(["Name", "Date", "Description", "Amount", "Category"])
        writer.writerow([name, date, description, amount, category])

    print("Expense logged successfully!")

def analyze_expenses():
    """Analyze expenses by family members and calculate average daily expense."""
    expenses = {}
    total_expenses = 0
    unique_dates = set()

    with open(EXPENSES_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"]
            amount = float(row["Amount"])
            date = row["Date"]

            if name not in expenses:
                expenses[name] = 0
            expenses[name] += amount
            total_expenses += amount
            unique_dates.add(date)

    print("\nExpense Analysis:")
    for name, total in expenses.items():
        print(f"{name}: Total Expenses = ₹{total:.2f}")

    avg_expense = total_expenses / len(unique_dates) if unique_dates else 0
    print(f"\nAverage Daily Expense for the Household: ₹{avg_expense:.2f}")

def plot_expense_trends():
    """Generate a line chart of cumulative expenses over the last month."""
    daily_totals = {}

    with open(EXPENSES_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row["Date"]
            amount = float(row["Amount"])
            if date not in daily_totals:
                daily_totals[date] = 0
            daily_totals[date] += amount

    sorted_dates = sorted(daily_totals.keys())
    cumulative_expenses = [sum(daily_totals[date] for date in sorted_dates[:i+1]) for i in range(len(sorted_dates))]

    plt.figure(figsize=(10, 5))
    plt.plot(sorted_dates, cumulative_expenses, marker="o")
    plt.title("Expense Trends Over Last Month")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Expenses (₹)")
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

def generate_monthly_report(month):
    """Generate a monthly expense report."""
    member_totals = {}
    category_totals = {}

    with open(EXPENSES_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row["Date"]
            if not date.startswith(month):  # Filter by the given month
                continue
            name = row["Name"]
            amount = float(row["Amount"])
            category = row["Category"]

            if name not in member_totals:
                member_totals[name] = 0
            member_totals[name] += amount

            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += amount

    print("\nMonthly Expense Report:")
    print("Total Expenses by Member:")
    for name, total in member_totals.items():
        print(f"{name}: ₹{total:.2f}")

    print("\nExpenses by Category:")
    for category, total in category_totals.items():
        print(f"{category}: ₹{total:.2f}")

def set_and_check_budget():
    """Set a budget for each category and warn if exceeded."""
    budgets = {}
    categories = set()

    with open(EXPENSES_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            categories.add(row["Category"])

    for category in categories:
        budgets[category] = float(input(f"Set a budget for {category}: ₹"))

    category_expenses = {category: 0 for category in categories}
    with open(EXPENSES_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = row["Category"]
            category_expenses[category] += float(row["Amount"])

    print("\nBudget Status:")
    for category, budget in budgets.items():
        expense = category_expenses[category]
        print(f"{category}: Spent ₹{expense:.2f}, Budget ₹{budget:.2f}")
        if expense > budget:
            print(f"Warning: Budget for {category} exceeded!")

def backup_data():
    """Backup the expenses.csv file."""
    backup_path = input("Enter backup file path (e.g., backup_expenses.csv): ").strip()
    shutil.copy(EXPENSES_FILE, backup_path)
    print(f"Backup saved to {backup_path}.")

def restore_data():
    """Restore the expenses.csv file from a backup."""
    backup_path = input("Enter backup file path: ").strip()
    try:
        shutil.copy(backup_path, EXPENSES_FILE)
        print(f"Data restored from {backup_path}.")
    except FileNotFoundError:
        print("Backup file not found.")

def main():
    """Main menu for the Household Expenses Tracker."""
    while True:
        print("\nHousehold Expenses Tracker")
        print("1. Log an Expense")
        print("2. Analyze Expenses")
        print("3. Plot Expense Trends")
        print("4. Generate Monthly Report")
        print("5. Set and Check Budget")
        print("6. Backup Data")
        print("7. Restore Data")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            log_expense()
        elif choice == "2":
            analyze_expenses()
        elif choice == "3":
            plot_expense_trends()
        elif choice == "4":
            month = input("Enter the month (YYYY-MM): ").strip()
            generate_monthly_report(month)
        elif choice == "5":
            set_and_check_budget()
        elif choice == "6":
            backup_data()
        elif choice == "7":
            restore_data()
        elif choice == "8":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
