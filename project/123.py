from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from employee import EmployeeClass
from supplier import SupplierClass
from category import CategoryClass
from product import ProductClasss
from sales import SalesClass
from login import LoginWindow
import sqlite3
import os
from datetime import datetime
class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        # Title
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT, font=("times new roman", 40, "bold"), bg="#010c48", fg="green", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout Button
        btn_logout = Button(self.root, text="Logout", command=self.logout, font=("times new roman", 15, "bold"), bg="yellow")
        btn_logout.place(x=1100, y=10, height=50, width=150)

        # Clock
        self.lbl_clock = Label(self.root, text=" Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time:HH:MM:SS", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.update_clock()

        # Left Menu
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        self.Menulogo = Image.open("images/menu_im.png")
        self.Menulogo = self.Menulogo.resize((200, 200))
        self.Menulogo = ImageTk.PhotoImage(self.Menulogo)

        lbl_menulogo = Label(LeftMenu, image=self.Menulogo)
        lbl_menulogo.pack(side=TOP, fill=X)

        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20,), bg="#009688")
        lbl_menu.pack(side=TOP, fill=X)

        btn_employee = Button(LeftMenu, text="Employee", command=self.employee, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_employee.pack(side=TOP, fill=X)

        btn_supplier = Button(LeftMenu, text="Supplier", command=self.supplier, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_supplier.pack(side=TOP, fill=X)

        btn_Category = Button(LeftMenu, text="Category", command=self.category, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_Category.pack(side=TOP, fill=X)

        btn_product = Button(LeftMenu, text="Product", command=self.product, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_product.pack(side=TOP, fill=X)

        btn_sales = Button(LeftMenu, text="Sales", command=self.sales, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_sales.pack(side=TOP, fill=X)

        btn_exit = Button(LeftMenu, text="Exit", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_exit.pack(side=TOP, fill=X)

        # Content
        self.lbl_employee = Label(self.root, text="Total Employee\n[0]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[0]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total Category\n[0]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=250)

        self.lbl_product = Label(self.root, text="Total Product\n[0]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Total Sales\n[0]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # Footer
        lbl_footer = Label(self.root, text=" IMS-Inventory Management System | Developed by  Aman,For Any Technical Issue Contact:98700004", font=("times new roman", 15), bg="#4d636d", fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.update_content()

    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {now.strftime('%d-%m-%Y')}\t\t Time:{now.strftime('%H:%M:%S')}")
        self.root.after(1000, self.update_clock)

    def logout(self):
        self.root.destroy()
        root_login = Tk()
        LoginWindow(root_login)
        root_login.mainloop()

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SupplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CategoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ProductClasss(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SalesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            employees = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[{len(employees)}]")

            cur.execute("SELECT * FROM supplier")
            suppliers = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[{len(suppliers)}]")

            cur.execute("SELECT * FROM category")
            categories = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[{len(categories)}]")

            cur.execute("SELECT * FROM product")
            products = cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[{len(products)}]")

            bill = len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales\n[{str(bill)}]')
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

        con.close()

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
