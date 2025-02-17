import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # pip install pillow

class CategoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Aman")
        self.root.config(bg="white")
        self.root.focus_force()

        # variables
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # title
        lbl_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30),
                          bg="#184a45", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

        # category name entry
        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 18), bg="white")
        lbl_name.place(x=50, y=100)
        self.txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 18), bg="lightyellow")
        self.txt_name.place(x=50, y=170, width=300)

        # buttons
        btn_add = Button(self.root, text="ADD", command=self.add_category,
                         font=("goudy old style", 15), bg="green", fg="white", cursor="hand2")
        btn_add.place(x=360, y=170, width=150, height=30)

        btn_delete = Button(self.root, text="Delete", command=self.delete_category,
                            font=("goudy old style", 15), bg="red", fg="white", cursor="hand2")
        btn_delete.place(x=520, y=170, width=150, height=30)

        # category details
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=100)

        scroll_y = Scrollbar(cat_frame, orient=VERTICAL)
        scroll_x = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.CategoryTable = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scroll_y.set,
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.CategoryTable.xview)
        scroll_y.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid", text="CID")
        self.CategoryTable.heading("name", text="Name")

        self.CategoryTable.pack(fill=BOTH, expand=1)

        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)

        # images
        self.im1 = Image.open("images/cat.jpg")
        self.im1 = self.im1.resize((500, 250))
        self.im1 = ImageTk.PhotoImage(self.im1)

        self.lbl_im1 = Label(self.root, image=self.im1, bd=2, relief=RAISED)
        self.lbl_im1.place(x=50, y=220)


        self.im2 = Image.open("images/category.jpg")
        self.im2 = self.im2.resize((500, 250))
        self.im2 = ImageTk.PhotoImage(self.im2)

        self.lbl_im2 = Label(self.root, image=self.im2, bd=2, relief=RAISED)
        self.lbl_im2.place(x=580, y=220)
        
        self.show_categories()  # Call the method to display categories

    def add_category(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            if self.var_name.get() == "":
                messagebox.showerror("Error","Category name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error","Category already present, please try a different one.", parent=self.root)
                else:
                    cur.execute("INSERT INTO category(name) VALUES (?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Category added successfully.", parent=self.root)
                    # Refresh category list
                    self.show_categories()  # Added this line to refresh the category list
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    

    def show_categories(self):
        try:
            con = sqlite3.connect(database=r'ims.db')    
            cur = con.cursor()
            cur.execute("SELECT * FROM category")  
            rows = cur.fetchall()  
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row)  
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def delete_category(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error","Please select  category  from the list", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row== None:
                    messagebox.showerror("Error","try again", parent=self.root)
                else:
                    op=messagebox.askyesno("confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","category Deleted Successfully",parent=self.root)
                        self.show_categories()  # Added this line to refresh the category list
                        self.var_cat_id.set("")
                        self.var_name.set("")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)                
                    
                              



    def get_data(self,ev):
        f=self.CategoryTable.focus() 
        content=(self.CategoryTable.item(f))  
        row=content['values']
        
        #print(row)
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])        


            

if __name__ == "__main__":
    root = Tk()
    obj = CategoryClass(root)
    root.mainloop()
