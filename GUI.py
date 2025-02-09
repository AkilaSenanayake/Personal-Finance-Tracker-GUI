import tkinter as tk
from tkinter import ttk
import json

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(' Personal Finance Tracker ')
        self.create_widgets()
        self.transactions = self.load_transactions('JSONfile.json')
        self.display_transactions(self.transactions)

    def create_widgets(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create frame for table and scrollbar
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for displaying transactions
        self.transaction_tree = ttk.Treeview(self.table_frame, columns=('Date', 'Amount', 'Category'), show='headings')
        for col in ("Date", "Amount", "Category"):
            self.transaction_tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c, False))
            self.transaction_tree.column(col, width=100, anchor=tk.CENTER)
            self.transaction_tree.heading(col, text=col + " ▾")

        # Custom style for the headings
        style = ttk.Style()
        style.theme_use("alt")

        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y) #Scrollbar to the right side
        self.transaction_tree.config(yscrollcommand=self.scrollbar.set)

        # Search bar, options, and button
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="Search Term:").grid(row=0, column=2)
        self.search_option = tk.StringVar(value="Contains")
        self.search_option_menu = ttk.OptionMenu(search_frame, self.search_option, "Contains", "Contains", "Exact Match")
        self.search_option_menu.grid(row=0, column=1, padx=5)

        ttk.Label(search_frame, text="Search Option:").grid(row=0, column=0)
        self.search_bar = ttk.Entry(search_frame, width=20)
        self.search_bar.grid(row=0, column=3, padx=5)

        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_transactions)
        self.search_button.grid(row=0, column=4, padx=5)

    def load_transactions(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                print("Loaded successfully")
                return data
        except FileNotFoundError:
            print("File not found.")
            return {}

    def display_transactions(self, transactions):
        # Clear existing entries
        self.transaction_tree.delete(*self.transaction_tree.get_children())

        # Add transactions to the treeview
        for category, trans_list in transactions.items():
            for transaction in trans_list:
                self.transaction_tree.insert("", "end", values=(transaction["date"], transaction["amount"], category))

    def search_transactions(self):
        search_term = self.search_bar.get().lower()
        search_option = self.search_option.get()

        filtered_transactions = []
        for category, trans_list in self.transactions.items():
            for transaction in trans_list:
                match = False
                if search_option == "Contains":
                    match = (search_term in transaction["date"].lower() or
                            search_term in str(transaction["amount"]).lower() or
                            search_term in category.lower())
                elif search_option == "Exact Match":
                    match = (search_term == transaction["date"].lower() or
                            search_term == str(transaction["amount"]).lower() or
                            search_term == category.lower())
                if match:
                    filtered_transactions.append((transaction["date"], transaction["amount"], category))

        # Clear existing entries
        self.transaction_tree.delete(*self.transaction_tree.get_children())

        # Add filtered transactions to the treeview
        for transaction in filtered_transactions:
            self.transaction_tree.insert("", "end", values=transaction)

    def sort_by_column(self, col, reverse):
        data = [(self.transaction_tree.set(child, col), child) for child in self.transaction_tree.get_children("")]
        data.sort(key=lambda x: float(x[0]), reverse=reverse) if col == "Amount" else data.sort(reverse=reverse)
        for index, item in enumerate(data):
            self.transaction_tree.move(item[1], "", index)
        # Toggle sorting direction for the next click
        current_direction = self.transaction_tree.heading(col, "text")[-1]
        new_direction = "▴" if current_direction == "▾" else "▾"
        self.transaction_tree.heading(col, text=col + " " + new_direction)

        self.transaction_tree.heading(col, command=lambda: self.sort_by_column(col, not reverse))
        data = [(self.transaction_tree.set(child, col), child) for child in self.transaction_tree.get_children("")]
        data.sort(key=lambda x: float(x[0]) if col == "Amount" else x[0], reverse=reverse)
        for index, item in enumerate(data):
            self.transaction_tree.move(item[1], "", index)

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
