import time
from datetime import datetime
import sys
import subprocess

def get_consent():
    while True:
        consent = input("Do you accept data collection? (yes/no): ").lower()
        if consent == "yes":
            return True
        elif consent == "no":
            print("Data collection rejected. Exiting program...")
            sys.exit()
        else:
            print("Please type 'yes' or 'no'.")

def get_cashier_name():
    return input("Enter cashier name: ").strip()

def record_sales():
    print("\nStart recording sales. Type 'done' when finished.\n")

    sales = {}  # {item: quantity}
    total_items = 0
    transactions = 0

    start_time = time.time()

    while True:
        item = input("Enter item name (or 'done'): ").strip()

        if item.lower() == "done":
            break

        try:
            quantity = int(input(f"Enter quantity for {item}: "))
        except ValueError:
            print("Invalid quantity. Try again.")
            continue

        # Update sales dictionary
        if item in sales:
            sales[item] += quantity
        else:
            sales[item] = quantity

        total_items += quantity
        transactions += 1

        print(f"{item} recorded.\n")

    end_time = time.time()
    duration = end_time - start_time

    return sales, total_items, transactions, duration

def save_log(cashier, sales, total_items, transactions, duration):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"Cashier: {cashier}\nDate: {date_time}\n"
    log_entry += f"Transactions: {transactions}\nTotal Items Sold: {total_items}\n"
    log_entry += f"Time Spent: {duration:.2f} seconds\n"
    log_entry += "Items Sold:\n"

    for item, qty in sales.items():
        log_entry += f" - {item}: {qty}\n"

    log_entry += "-" * 40 + "\n"
    subprocess.run(
        ["bash", "-c", "cats >> shop_logs.txt"],
        input=log_entry,
        text=True
    )
    

def main():
    print("Welcome to Shop Management System\n")

    if not get_consent():
        return

    cashier = get_cashier_name()

    sales, total_items, transactions, duration = record_sales()

    print("\nSession Summary:")
    print(f"Cashier: {cashier}")
    print(f"Transactions: {transactions}")
    print(f"Total Items Sold: {total_items}")
    print(f"Time Spent: {duration:.2f} seconds")

    save_log(cashier, sales, total_items, transactions, duration)

    print("\nProgram exited")

if __name__ == "__main__":
    main()
