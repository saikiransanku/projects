import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import date, datetime
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from reportlab.pdfgen import canvas

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
        self.root.geometry("1000x600")
        self.dark_mode = False

        # ---------------- Slide Panel Setup ----------------
        self.panel_width = 260
        self.panel = tk.Frame(self.root, width=self.panel_width, height=600, bg="#ECECEC")
        self.panel.place(x=-self.panel_width, y=0)
        self.panel_open = False

        self.create_slide_panel()

        toggle_btn = tk.Button(root, text="☰ Month Panel", bg="#455A64", fg="white",
                               command=self.toggle_panel)
        toggle_btn.place(x=10, y=10)

        # ---------------- Existing UI ----------------
        title = tk.Label(root, text="Personal Expense Tracker",
                         font=("Arial", 20, "bold"))
        title.pack(pady=40)

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

    # ---------------- SLIDE PANEL UI ----------------
    def create_slide_panel(self):
        tk.Label(self.panel, text="Month Selection", bg="#ECECEC", font=("Arial", 14, "bold")).pack(pady=20)

        years = [str(y) for y in range(2020, 2031)]
        months = [str(m).zfill(2) for m in range(1, 13)]

        tk.Label(self.panel, text="Year:", bg="#ECECEC").pack()
        self.sel_year = ttk.Combobox(self.panel, values=years, state="readonly")
        self.sel_year.current(0)
        self.sel_year.pack(pady=5)

        tk.Label(self.panel, text="Month:", bg="#ECECEC").pack()
        self.sel_month = ttk.Combobox(self.panel, values=months, state="readonly")
        self.sel_month.current(0)
        self.sel_month.pack(pady=5)

        tk.Button(self.panel, text="📥 Load Month", bg="#1976D2", fg="white",
                  command=self.load_month).pack(pady=10)

        tk.Label(self.panel, text="Add Expense", bg="#ECECEC", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(self.panel, text="Day (DD):", bg="#ECECEC").pack()
        self.day_entry = tk.Entry(self.panel)
        self.day_entry.pack(pady=2)

        tk.Label(self.panel, text="Category:", bg="#ECECEC").pack()
        self.cat_entry = tk.Entry(self.panel)
        self.cat_entry.pack(pady=2)

        tk.Label(self.panel, text="Description:", bg="#ECECEC").pack()
        self.desc_entry = tk.Entry(self.panel)
        self.desc_entry.pack(pady=2)

        tk.Label(self.panel, text="Amount (₹):", bg="#ECECEC").pack()
        self.amount_add = tk.Entry(self.panel)
        self.amount_add.pack(pady=2)

        tk.Button(self.panel, text="➕ Add to Month", bg="#43A047", fg="white",
                  command=self.add_to_month).pack(pady=10)

        tk.Button(self.panel, text="✏ Edit Selected", bg="#FFA000", fg="white",
                  command=self.edit_selected).pack(pady=5)

        tk.Button(self.panel, text="🗑 Delete Selected", bg="#D32F2F", fg="white",
                  command=self.delete_expense).pack(pady=5)

    # ---------------- PANEL ANIMATION ----------------
    def toggle_panel(self):
        if self.panel_open:
            self.hide_panel()
        else:
            self.show_panel()

    def show_panel(self):
        x = -self.panel_width
        while x < 0:
            self.panel.place(x=x, y=0)
            x += 20
            self.panel.update()
        self.panel_open = True

    def hide_panel(self):
        x = 0
        while x > -self.panel_width:
            self.panel.place(x=x, y=0)
            x -= 20
            self.panel.update()
        self.panel_open = False

    # ---------------- MONTH FUNCTIONS ----------------
    def load_month(self):
        year = self.sel_year.get()
        month = self.sel_month.get()
        pattern = f"{year}-{month}%"

        for i in self.tree.get_children():
            self.tree.delete(i)

        cursor.execute("SELECT date,category,description,amount FROM expenses WHERE date LIKE ?", (pattern,))
        rows = cursor.fetchall()
        for r in rows:
            self.tree.insert("", tk.END, values=r)

    def add_to_month(self):
        year = self.sel_year.get()
        month = self.sel_month.get()
        day = self.day_entry.get().zfill(2)
        date_val = f"{year}-{month}-{day}"

        category = self.cat_entry.get()
        desc = self.desc_entry.get()

        try:
            amount = float(self.amount_add.get())
        except:
            messagebox.showerror("Error", "Invalid amount")
            return

        cursor.execute("INSERT INTO expenses(date,category,description,amount) VALUES(?,?,?,?)",
                       (date_val, category, desc, amount))
        conn.commit()

        messagebox.showinfo("Done", "Added to month")
        self.load_month()

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a row")
            return

        values = self.tree.item(sel)["values"]

        new_date = tk.simpledialog.askstring("Edit", "Enter new date:", initialvalue=values[0])
        new_cat = tk.simpledialog.askstring("Edit", "Enter new category:", initialvalue=values[1])
        new_desc = tk.simpledialog.askstring("Edit", "Enter new desc:", initialvalue=values[2])
        new_amt = tk.simpledialog.askstring("Edit", "Enter new amount:", initialvalue=values[3])

        cursor.execute("""
            UPDATE expenses SET date=?,category=?,description=?,amount=?
            WHERE date=? AND category=? AND description=? AND amount=?
        """,
                       (new_date, new_cat, new_desc, new_amt,
                        values[0], values[1], values[2], values[3]))

        conn.commit()
        messagebox.showinfo("Updated", "Record updated!")
        self.load_month()

    # ---------------- EXISTING FUNCTIONS (unchanged) ----------------
    def add_expense(self):
        date_val = self.date_entry.get()
        category = self.category_entry.get()
        desc = self.desc_entry.get()

        try:
            amount = float(self.amount_entry.get())
        except:
            messagebox.showerror("Invalid Input", "Enter a valid amount.")
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
        self.view_expenses()

    def show_summary(self):
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0] or 0
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = cursor.fetchall()

        msg = f"Total: ₹{total:.2f}\n\n"
        for cat, amt in data:
            msg += f"{cat}: ₹{amt:.2f}\n"

        messagebox.showinfo("Summary", msg)

    def show_graph(self):
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = cursor.fetchall()
        if not data:
            messagebox.showwarning("No Data", "No expenses found.")
            return

        labels = [x[0] for x in data]
        vals = [x[1] for x in data]

        plt.bar(labels, vals)
        plt.show()

    def show_monthly_graph(self):
        cursor.execute("""
            SELECT substr(date,1,7), SUM(amount)
            FROM expenses
            GROUP BY substr(date,1,7)
            ORDER BY substr(date,1,7)
        """)
        data = cursor.fetchall()

        if not data:
            messagebox.showwarning("No Data", "No data")
            return

        months = [x[0] for x in data]
        totals = [x[1] for x in data]
        plt.plot(months, totals, marker="o")
        plt.show()

    def show_pie_chart(self):
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = cursor.fetchall()
        labels = [x[0] for x in data]
        vals = [x[1] for x in data]
        plt.pie(vals, labels=labels, autopct="%1.1f%%")
        plt.show()

    def export_excel(self):
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()

        wb = Workbook()
        ws = wb.active
        ws.append(["ID", "Date", "Category", "Description", "Amount"])

        for r in rows:
            ws.append(r)

        file = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if file:
            wb.save(file)

    def export_pdf(self):
        cursor.execute("SELECT date,category,description,amount FROM expenses")
        rows = cursor.fetchall()

        file = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not file:
            return

        pdf = canvas.Canvas(file)
        y = 800
        for r in rows:
            pdf.drawString(50, y, str(r))
            y -= 20
            if y < 50:
                pdf.showPage()
                y = 800
        pdf.save()

    def filter_by_date(self):
        f = self.from_date.get()
        t = self.to_date.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor.execute("SELECT date,category,description,amount FROM expenses WHERE date BETWEEN ? AND ?", (f, t))
        data = cursor.fetchall()
        for r in data:
            self.tree.insert("", tk.END, values=r)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

    def clear_fields(self):
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

root = tk.Tk()
app = ExpenseTracker(root)
root.mainloop()
conn.close()
