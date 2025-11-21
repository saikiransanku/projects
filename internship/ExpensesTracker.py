import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

# -------------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------------
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    description TEXT,
    amount REAL
)
""")
conn.commit()

# -------------------------------------------------------
# MAIN APP CLASS
# -------------------------------------------------------
class ExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("💰 Personal Expense Tracker")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # ---------------- Title ----------------
        title = tk.Label(root, text="Personal Expense Tracker",
                         font=("Arial", 18, "bold"), fg="#1E88E5")
        title.pack(pady=10)

        # ---------------- Input Frame ----------------
        input_frame = tk.Frame(root, padx=10, pady=10)
        input_frame.pack(fill="x")

        # Date
        tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)
        self.date_entry.insert(0, str(date.today()))

        # Category
        tk.Label(input_frame, text="Category:").grid(row=1, column=0, sticky="w")
        self.category_entry = tk.Entry(input_frame)
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)

        # Description
        tk.Label(input_frame, text="Description:").grid(row=2, column=0, sticky="w")
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=2, column=1, padx=10, pady=5)

        # Amount
        tk.Label(input_frame, text="Amount (₹):").grid(row=3, column=0, sticky="w")
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=5)

        # Add Button
        add_btn = tk.Button(input_frame, text="➕ Add Expense", bg="#43A047", fg="white",
                            command=self.add_expense)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # ---------------- Table Frame ----------------
        table_frame = tk.Frame(root)
        table_frame.pack(pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame,
                                 columns=("Date", "Category", "Description", "Amount"),
                                 show="headings")

        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount (₹)")

        self.tree.column("Date", width=100)
        self.tree.column("Category", width=100)
        self.tree.column("Description", width=300)
        self.tree.column("Amount", width=100)

        self.tree.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ---------------- Buttons Frame ----------------
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        view_btn = tk.Button(btn_frame, text="📄 View All", bg="#1976D2", fg="white",
                             command=self.view_expenses)
        view_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(btn_frame, text="🗑 Delete Selected", bg="#E53935", fg="white",
                               command=self.delete_expense)
        delete_btn.grid(row=0, column=1, padx=10)

        summary_btn = tk.Button(btn_frame, text="📊 Show Summary", bg="#F9A825", fg="black",
                                command=self.show_summary)
        summary_btn.grid(row=0, column=2, padx=10)

        # Load existing data
        self.view_expenses()

    # ---------------------------------------------------
    # FUNCTIONS
    # ---------------------------------------------------
    def add_expense(self):
        date_val = self.date_entry.get()
        category = self.category_entry.get()
        desc = self.desc_entry.get()

        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        if not category or not desc:
            messagebox.showwarning("Missing Fields", "Please fill all fields.")
            return

        cursor.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                       (date_val, category, desc, amount))
        conn.commit()

        messagebox.showinfo("Success", "Expense added successfully!")
        self.clear_fields()
        self.view_expenses()

    def view_expenses(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        cursor.execute("SELECT date, category, description, amount FROM expenses ORDER BY date DESC")
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select an Item", "Please select a record to delete.")
            return

        values = self.tree.item(selected_item)["values"]
        date_val, category, desc, amount = values

        cursor.execute("DELETE FROM expenses WHERE date=? AND category=? AND description=? AND amount=?",
                       (date_val, category, desc, amount))
        conn.commit()

        messagebox.showinfo("Deleted", "Expense record deleted successfully!")
        self.view_expenses()

    def show_summary(self):
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0

        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        cat_summary = cursor.fetchall()

        summary_text = f"💰 Total Expenses: ₹ {total:.2f}\n\n"

        for cat, amt in cat_summary:
            summary_text += f"{cat}: ₹ {amt:.2f}\n"

        messagebox.showinfo("Expense Summary", summary_text)

    def clear_fields(self):
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, str(date.today()))

# -------------------------------------------------------
# RUN APP
# -------------------------------------------------------
root = tk.Tk()
app = ExpenseTracker(root)
root.mainloop()

conn.close()
