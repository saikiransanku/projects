import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import date, datetime
import matplotlib.pyplot as plt
from openpyxl import Workbook
from reportlab.pdfgen import canvas

# -----------------------------------------
# DATABASE SETUP
# -----------------------------------------
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

class ExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("💰 Personal Expense Tracker ")
        self.root.geometry("900x600")

        self.dark_mode = False

        title = tk.Label(root, text="Personal Expense Tracker",
                         font=("Arial", 20, "bold"))
        title.pack(pady=10)

        input_frame = tk.Frame(root, padx=10, pady=10)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=10)
        self.date_entry.insert(0, str(date.today()))

        tk.Label(input_frame, text="Category:").grid(row=1, column=0)
        self.category_entry = tk.Entry(input_frame)
        self.category_entry.grid(row=1, column=1, padx=10)

        tk.Label(input_frame, text="Description:").grid(row=2, column=0)
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=2, column=1, padx=10)

        tk.Label(input_frame, text="Amount (₹):").grid(row=3, column=0)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=3, column=1, padx=10)

        add_btn = tk.Button(input_frame, text="➕ Add Expense",
                            bg="#43A047", fg="white",
                            command=self.add_expense)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="From:").grid(row=0, column=0)
        self.from_date = tk.Entry(filter_frame)
        self.from_date.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="To:").grid(row=0, column=2)
        self.to_date = tk.Entry(filter_frame)
        self.to_date.grid(row=0, column=3, padx=5)

        filter_btn = tk.Button(filter_frame, text="🔍 Filter",
                               command=self.filter_by_date)
        filter_btn.grid(row=0, column=4, padx=5)

        reset_btn = tk.Button(filter_frame, text="🔄 Reset",
                              command=self.view_expenses)
        reset_btn.grid(row=0, column=5, padx=5)

        table_frame = tk.Frame(root)
        table_frame.pack(pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame,
                                 columns=("Date", "Category", "Description", "Amount"),
                                 show="headings")

        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount (₹)")

        self.tree.column("Date", width=120)
        self.tree.column("Category", width=120)
        self.tree.column("Description", width=300)
        self.tree.column("Amount", width=120)

        self.tree.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="📄 View All", bg="#1976D2", fg="white",
                  command=self.view_expenses).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="🗑 Delete Selected", bg="#E53935", fg="white",
                  command=self.delete_expense).grid(row=0, column=1, padx=10)

        tk.Button(btn_frame, text="📊 Summary", bg="#F9A825", fg="black",
                  command=self.show_summary).grid(row=0, column=2, padx=10)

        tk.Button(btn_frame, text="📈 Category Graph", bg="#8E24AA", fg="white",
                  command=self.show_graph).grid(row=0, column=3, padx=10)

        tk.Button(btn_frame, text="📆 Monthly Line Graph", bg="#5E35B1", fg="white",
                  command=self.show_monthly_graph).grid(row=0, column=4, padx=10)

        tk.Button(btn_frame, text="🧁 Pie Chart", bg="#FF7043", fg="white",
                  command=self.show_pie_chart).grid(row=0, column=5, padx=10)

        tk.Button(btn_frame, text="📤 Export Excel", bg="#00ACC1", fg="white",
                  command=self.export_excel).grid(row=0, column=6, padx=10)

        tk.Button(btn_frame, text="📑 PDF Report", bg="#6D4C41", fg="white",
                  command=self.export_pdf).grid(row=0, column=7, padx=10)

        tk.Button(btn_frame, text="🌙 Dark Mode", bg="#212121", fg="white",
                  command=self.toggle_dark_mode).grid(row=0, column=8, padx=10)

        self.view_expenses()

    def add_expense(self):
        date_val = self.date_entry.get()
        category = self.category_entry.get()
        desc = self.desc_entry.get()

        try:
            amount = float(self.amount_entry.get())
        except:
            messagebox.showerror("Invalid Input", "Enter a valid amount.")
            return

        if not category or not desc:
            messagebox.showwarning("Missing", "Fill all fields.")
            return

        cursor.execute("INSERT INTO expenses(date, category, description, amount) VALUES (?, ?, ?, ?)",
                       (date_val, category, desc, amount))
        conn.commit()

        messagebox.showinfo("Success", "Expense added!")
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
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a record to delete.")
            return

        values = self.tree.item(selected)["values"]
        cursor.execute("DELETE FROM expenses WHERE date=? AND category=? AND description=? AND amount=?",
                       values)
        conn.commit()

        messagebox.showinfo("Deleted", "Record deleted!")
        self.view_expenses()

    def show_summary(self):
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0

        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = cursor.fetchall()

        msg = f"Total Expenses: ₹{total:.2f}\n\n"
        for cat, amt in data:
            msg += f"{cat}: ₹{amt:.2f}\n"

        messagebox.showinfo("Summary", msg)

    def show_graph(self):
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = cursor.fetchall()

        if not data:
            messagebox.showwarning("No Data", "No expenses found.")
            return

        categories = [x[0] for x in data]
        amounts = [x[1] for x in data]

        plt.figure(figsize=(8, 5))
        plt.bar(categories, amounts)
        plt.title("Category-wise Expenses")
        plt.xlabel("Category")
        plt.ylabel("Total (₹)")
        plt.show()

    def show_monthly_graph(self):
        cursor.execute("""
            SELECT SUBSTR(date, 1, 7), SUM(amount)
            FROM expenses
            GROUP BY SUBSTR(date, 1, 7)
            ORDER BY SUBSTR(date, 1, 7)
        """)
        data = cursor.fetchall()

        if not data:
            messagebox.showwarning("No Data", "No expenses found.")
            return

        months = [x[0] for x in data]
        totals = [x[1] for x in data]

        plt.figure(figsize=(8, 5))
        plt.plot(months, totals, marker="o")
        plt.title("Monthly Expense Trend")
        plt.xlabel("Month")
        plt.ylabel("Total (₹)")
        plt.grid(True)
        plt.show()

    def show_pie_chart(self):
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = cursor.fetchall()

        if not data:
            messagebox.showwarning("No Data", "No expenses found.")
            return

        labels = [x[0] for x in data]
        values = [x[1] for x in data]

        plt.figure(figsize=(7, 7))
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title("Expense Distribution (Pie Chart)")
        plt.show()

    def export_excel(self):
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()

        wb = Workbook()
        ws = wb.active
        ws.append(["ID", "Date", "Category", "Description", "Amount"])

        for row in rows:
            ws.append(row)

        file = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if file:
            wb.save(file)
            messagebox.showinfo("Saved", "Exported to Excel successfully!")

    def export_pdf(self):
        cursor.execute("SELECT date, category, description, amount FROM expenses")
        rows = cursor.fetchall()

        file = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not file:
            return

        pdf = canvas.Canvas(file)
        pdf.setFont("Helvetica", 12)

        y = 800
        pdf.drawString(100, y, "Expense Report")
        y -= 30

        for row in rows:
            pdf.drawString(50, y, f"{row}")
            y -= 20

            if y < 50:
                pdf.showPage()
                y = 800

        pdf.save()
        messagebox.showinfo("Saved", "PDF Report Generated!")

    def filter_by_date(self):
        f = self.from_date.get()
        t = self.to_date.get()

        try:
            cursor.execute("SELECT date, category, description, amount FROM expenses WHERE date BETWEEN ? AND ?", (f, t))
            data = cursor.fetchall()
        except:
            messagebox.showerror("Error", "Invalid date format.")
            return

        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in data:
            self.tree.insert("", tk.END, values=row)

    def toggle_dark_mode(self):
        bg = "#121212" if not self.dark_mode else "white"
        fg = "white" if not self.dark_mode else "black"

        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass

        self.dark_mode = not self.dark_mode
    def clear_fields(self):
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
root = tk.Tk()
app = ExpenseTracker(root)
root.mainloop()

conn.close()
