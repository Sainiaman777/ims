from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from employee import EmployeeClass
from supplier import SupplierClass
from category import CategoryClass
from product import ProductClasss
from billing import BillClass
from sales import SalesClass
import sqlite3
import os
from datetime import datetime

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x350+500+200")
        self.root.config(bg="white")

        # Frame
        frame = Frame(self.root, bg="white")
        frame.place(x=50, y=50, width=300, height=260)

        # Title
        title = Label(frame, text="Login System", font=("times new roman", 20, "bold"), bg="white", fg="black")
        title.place(x=0, y=20, relwidth=1)

        # Username
        lbl_user = Label(frame, text="Username", font=("times new roman", 15, "bold"), bg="white", fg="black")
        lbl_user.place(x=20, y=70)
        self.txt_user = Entry(frame, font=("times new roman", 15), bg="lightgray")
        self.txt_user.place(x=20, y=100, width=250)

        # Password
        lbl_pass = Label(frame, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="black")
        lbl_pass.place(x=20, y=140)
        self.txt_pass = Entry(frame, font=("times new roman", 15), bg="lightgray", show='*')
        self.txt_pass.place(x=20, y=170, width=250)

        # Login Button
        btn_login = Button(frame, text="Login", command=self.login, font=("times new roman", 15, "bold"), bg="blue", fg="white", cursor="hand2")
        btn_login.place(x=20, y=210, width=250)

        # Signup Button
        btn_signup = Button(self.root, text="Sign Up", command=self.signup_window, font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2")
        btn_signup.place(x=150, y=310, width=100)

    def login(self):
        if self.txt_user.get() == "" or self.txt_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (self.txt_user.get(), self.txt_pass.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", "Welcome!", parent=self.root)
                    self.root.destroy()
                    self.open_ims()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

    def signup_window(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SignupWindow(self.new_win)

    def open_ims(self):
        root_ims = Tk()
        IMS(root_ims)
        root_ims.mainloop()

class SignupWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")
        self.root.geometry("400x400+500+200")
        self.root.config(bg="white")

        # Frame
        frame = Frame(self.root, bg="white")
        frame.place(x=50, y=50, width=300, height=300)

        # Title
        title = Label(frame, text="Sign Up", font=("times new roman", 20, "bold"), bg="white", fg="black")
        title.place(x=0, y=20, relwidth=1)

        # Username
        lbl_user = Label(frame, text="Username", font=("times new roman", 15, "bold"), bg="white", fg="black")
        lbl_user.place(x=20, y=70)
        self.txt_user = Entry(frame, font=("times new roman", 15), bg="lightgray")
        self.txt_user.place(x=20, y=100, width=250)

        # Password
        lbl_pass = Label(frame, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="black")
        lbl_pass.place(x=20, y=140)
        self.txt_pass = Entry(frame, font=("times new roman", 15), bg="lightgray", show='*')
        self.txt_pass.place(x=20, y=170, width=250)

        # Confirm Password
        lbl_cpass = Label(frame, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white", fg="black")
        lbl_cpass.place(x=20, y=210)
        self.txt_cpass = Entry(frame, font=("times new roman", 15), bg="lightgray", show='*')
        self.txt_cpass.place(x=20, y=240, width=250)

        # Signup Button
        btn_signup = Button(frame, text="Sign Up", command=self.signup, font=("times new roman", 15, "bold"), bg="green", fg="white", cursor="hand2")
        btn_signup.place(x=20, y=270, width=250)

    def signup(self):
        if self.txt_user.get() == "" or self.txt_pass.get() == "" or self.txt_cpass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.txt_pass.get() != self.txt_cpass.get():
            messagebox.showerror("Error", "Password & Confirm Password should be same", parent=self.root)
        else:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                cur.execute("SELECT * FROM admin")
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Admin already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (self.txt_user.get(), self.txt_pass.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Admin account created successfully", parent=self.root)
                    self.root.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

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

        btn_category = Button(LeftMenu, text="Category", command=self.category, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_category.pack(side=TOP, fill=X)

        btn_product = Button(LeftMenu, text="Products", command=self.product, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_product.pack(side=TOP, fill=X)

        btn_sales = Button(LeftMenu, text="Sales", command=self.sales, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_sales.pack(side=TOP, fill=X)

        btn_billing = Button(LeftMenu, text="Billing", command=self.billing, font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_billing.pack(side=TOP, fill=X)

        # Content
        self.lbl_employee = Label(self.root, text="Total Employee\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[ 0 ]", bd=5, relief=RIDGE, bg="#ff5722", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total Category\n[ 0 ]", bd=5, relief=RIDGE, bg="#009688", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=250)

        self.lbl_product = Label(self.root, text="Total Products\n[ 0 ]", bd=5, relief=RIDGE, bg="#607d8b", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Total Sales\n[ 0 ]", bd=5, relief=RIDGE, bg="#ffc107", fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # Footer
        lbl_footer = Label(self.root, text="IMS-Inventory Management System | Developed by Aman saini For any technical issue contact: as801250@gmail,.com", font=("times new roman", 12), bg="#4d636d", fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)

    def update_clock(self):
        now = datetime.now()
        date_str = now.strftime('%d-%m-%Y')
        time_str = now.strftime('%H:%M:%S')
        self.lbl_clock.config(text=f" Welcome to Inventory Management System\t\t Date: {date_str}\t\t Time:{time_str}")
        self.lbl_clock.after(1000, self.update_clock)

    def logout(self):
        op = messagebox.askyesno("Logout", "Do you really want to logout?", parent=self.root)
        if op:
            self.root.destroy()
            self.__init__()

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

    def billing(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = BillClass(self.new_win)




if __name__ == "__main__":
    root = Tk()
    obj = LoginWindow(root)
    root.mainloop()

