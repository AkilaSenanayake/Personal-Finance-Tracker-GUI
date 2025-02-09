import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import GUI


#Global dictionary to store transactions
transactions = {}

# File handling functions

def load_transactions():     #Function to load transactions from a JSON file
    global transactions
    try:
        with open('JSONFile', 'r') as file:  #Try to open the file in read mode
            transactions = json.load(file)  #Load the json data from the file
    except FileNotFoundError:
        pass

#function to save transaction data to a json file
def save_transactions():
    with open('JSONFile.json', 'w') as file:  #Try to open the file in write mode
        json.dump(transactions, file, indent= 4)  #This function saves user inputs into a json file

# Function to read bulk transactions from a file
def read_bulk_transactions_from_file(filename):
    global transactions
    try:
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                transaction_type = data[0].strip().capitalize()
                amount = float(data[1].strip())
                date = data[2].strip()
                if transaction_type in transactions:
                    transactions[transaction_type].append({'amount': amount, 'date': date})
                else:
                    transactions[transaction_type] = [{'amount': amount, 'date': date}]
            print('Transactions successfully loaded!')
    
    except FileNotFoundError:
        print('File not found.')

# Feature implementations

#function to add a new transaction
def add_transaction():
    global transactions
    while True:          #Loop indefinitely until a valid amount is entered
        try:
            amount = float(input('Enter the amount : '))
            if amount <= 0:
                print('Enter the amount greater than zero.')
                continue
        except ValueError:
            print("Invalid amount. Please enter a number.")
            continue
        else:
            break

    #get the transaction category from the user
    category = input('Enter category : ').capitalize()  #prompt the user to select type
    while True:
        type_ = input('Enter the type (Income/Expense) : ').capitalize()
        if type_ in ['Income', 'Expense']:
            break
        else:
            print("Invalid type. Please enter 'Income' or 'Expense'.")

    while True:
        try:
            date = datetime.strptime(input('Enter date (YYYY-MM-DD): '), "%Y-%m-%d")  #get the transaction date from the user
        except ValueError:
            print('Invalid date format. Please enter in YYYY-MM-DD format.')
        else:
            break

    #get transaction category from the user
    if category in transactions:
        transactions[category].append({'amount': amount, 'date': date.strftime("%Y-%m-%d")})
    else:
        transactions[category] = [{'amount': amount, 'date': date.strftime("%Y-%m-%d")}]
    print('Transaction added successfully.')
    save_transactions()  #save the updated transaction list to the json file


#function to view all transactions
def view_transactions():
    global transactions
    if not transactions:
        print('No transactions')
    else:
        for category, category_transactions in transactions.items():
            print(f"{category}:")
            for transaction in category_transactions:
                print(f"Amount: {transaction['amount']} | Date: {transaction['date']}")
            print()

#function to update transactions
def update_transaction():
    global transactions
    view_transactions()
    if not transactions:  #Check if there are no transaction
        print('No transactions to update.')
        return
    category = input('Enter category to update : ').capitalize()
    if category in transactions:
        print(f"Transactions of category '{category}':")
        for i, transaction in enumerate(transactions[category]):
            print(f"{i + 1}. Amount: {transaction['amount']} | Date: {transaction['date']}")
        try:
            choice = int(input('Enter transaction number to update : ')) - 1
            if 0 <= choice < len(transactions[category]):
                amount = float(input('Enter updated amount: '))
                date = input('Enter updated date (YYYY-MM-DD): ')
                transactions[category][choice] = {'amount': amount, 'date': date}
                print('Transaction updated successfully.')
                save_transactions()
            else:
                print('Invalid transaction number.')
        except ValueError:
            print('Invalid transaction number.')
    else:
        print(f"No transactions found for category '{category}'.")


#function to delete transaction
def delete_transaction():
    global transactions
    view_transactions()  #Display all transactions
    if not transactions:  #check if there are no transactions
        print('No transactions to delete.')
        return
    category = input('Enter category to delete : ').capitalize()
    if category in transactions:
        print(f"Transactions of category '{category}':")
        for i, transaction in enumerate(transactions[category]):
            print(f"{i + 1}. Amount: {transaction['amount']} | Date : {transaction['date']}")
        try:
            choice = int(input('Enter transaction number to delete : ')) - 1
            if 0 <= choice < len(transactions[category]):
                del transactions[category][choice]
                print('Transaction successfully deleted.')
                save_transactions()
            else:
                print('Invalid transaction number.')
        except ValueError:
            print('Invalid transaction number.')
    else:
        print(f"No transactions found for category '{category}'.")


#function to display a summary of transactions
def display_summary():
    global transactions
    print('Summary:')
    print('\n')
    for expense_type, transactions_list in transactions.items():
        total_amount = sum(transaction["amount"] for transaction in transactions_list)
        print(expense_type + ":",total_amount)


#function for the main menu of the program
def main_menu():
    load_transactions()   # Load transactions at the start
    while True:
        print('\nPersonal Finance Tracker ')
        print('1. Add Transaction')
        print('2. View Transactions')
        print('3. Update Transaction')
        print('4. Delete Transaction')
        print('5. View Summary')
        print('6. Read Bulk Transactions from File')
        print('7. Open the GUI')
        print('8. Save and Exit')
        choice = input('Enter your choice : ')

        if choice == '1':  #if the user chooses to add a transaction
            add_transaction()  #call the add_transaction function
        elif choice == '2':  #if the user chooses to view transaction
            view_transactions()  #call the view_transaction function
        elif choice == '3':  #if the user chooses to update transcation
            update_transaction()  #call the update_transaction function
        elif choice == '4':  #if the user chooses to delete  a transaction
            delete_transaction()  #call the display_transaction function
        elif choice == '5':  #if the user chooses to display a summary
            display_summary()  #call the display_summary function
        elif choice == '6':
            filename = input('Enter filename : ')
            read_bulk_transactions_from_file(filename)
            save_transactions()
        elif choice == '7':
            root = tk.Tk()  # Create a Tkinter root window
            GUI.FinanceTrackerGUI(root)  # Create an instance of the GUI class
            root.mainloop()
        elif choice == '8':  #if the user chooses to exit
            save_transactions()
            print('Transactions saved. Thank you!!')
            break
        else:
            print('Invalid choice. Try again.')

if __name__ == "__main__":  #if the script is run as the main program
    main_menu()  #Call the main_menu function to start the application
