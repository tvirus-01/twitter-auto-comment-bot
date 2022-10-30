import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser
from tkinter import *
from scraper.classScraper import Scraper

from db import db

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Twitter Commenter')
        
        # # Fullscreen
        # master.attributes("-fullscreen", True)
        # master.bind("<Escape>", self.end_fullscreen)

        #tabs
        self.tabControl = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tabControl, )
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text ='Dashboard')
        self.tabControl.add(self.tab2, text ='Users')
        self.tabControl.pack(expand = 1, fill ="both")

        mygreen = "#d2ffd2"
        myred = "#dd0202"
        self.bgColor = "#d9d9d9"

        style = ttk.Style()
        style.theme_create( "yummy", parent="alt", settings={
                "TNotebook": {
                    "configure": {
                        "tabmargins": [2, 5, 2, 0],
                        "background": mygreen
                        } 
                    },
                "TNotebook.Tab": {
                    "configure": {
                        "padding": [5, 1], 
                        "background": mygreen 
                        },
                    "map": {
                        "background": [("selected", myred)],
                        "expand": [("selected", [1, 1, 1, 0])] 
                        } 
                    } 
                } )
        style.theme_use("yummy")

        self.create_widgets()
        self.populate_list()

    def end_fullscreen(self, event=None):
        self.master.attributes("-fullscreen", False)
        return "break"


    def create_widgets(self):
        # User Name
        self.part_text = tk.StringVar()
        self.part_label = tk.Label(
            self.tab1, text='User Name', font=('bold', 14), pady=20, padx=5, background=self.bgColor, foreground="black")
        self.part_label.grid(row=0, column=0, sticky=tk.W)
        self.part_entry = tk.Entry(self.tab1, textvariable=self.part_text, background=self.bgColor, foreground="black")
        self.part_entry.grid(row=0, column=1)
        # Email
        self.customer_text = tk.StringVar()
        self.customer_label = tk.Label(
            self.tab1, text='Email', font=('bold', 14), padx=5, background=self.bgColor, foreground="black")
        self.customer_label.grid(row=0, column=2, sticky=tk.W)
        self.customer_entry = tk.Entry(
            self.tab1, textvariable=self.customer_text, background=self.bgColor, foreground="black")
        self.customer_entry.grid(row=0, column=3)
        # Password
        self.retailer_text = tk.StringVar()
        self.retailer_label = tk.Label(
            self.tab1, text='Password', font=('bold', 14), padx=5, background=self.bgColor, foreground="black")
        self.retailer_label.grid(row=1, column=0, sticky=tk.W)
        self.retailer_entry = tk.Entry(
            self.tab1, textvariable=self.retailer_text, background=self.bgColor, foreground="black")
        self.retailer_entry.grid(row=1, column=1)
        # Confirm Password
        self.conPass_text = tk.StringVar()
        self.conPass_label = tk.Label(
            self.tab1, text='Confirm Password', font=('bold', 14), padx=5, background=self.bgColor, foreground="black")
        self.conPass_label.grid(row=1, column=2, sticky=tk.W)
        self.conPass_entry = tk.Entry(
            self.tab1, textvariable=self.conPass_text, background=self.bgColor, foreground="black")
        self.conPass_entry.grid(row=1, column=3)

        # Tweet Comment
        self.comment_text = tk.StringVar()
        self.comment_label = tk.Label(
            self.tab1, text='Tweet Comment', font=('bold', 14), pady=10, padx=5, background=self.bgColor, foreground="black")
        self.comment_label.grid(row=2, column=0, sticky=tk.W)
        self.comment_entry = tk.Text(
            self.tab1, width=50, height=20, background=self.bgColor, foreground="black")
        self.comment_entry.grid(row=2, column=1, pady=40)

        # Tweet hashtag
        self.hashtag_text = tk.StringVar()
        self.hashtag_label = tk.Label(
            self.tab1, text='Hashtags \n (use , after each hashtag)', font=('bold', 11), pady=10, padx=5, background=self.bgColor, foreground="black")
        self.hashtag_label.grid(row=2, column=3, sticky=tk.W)
        self.hashtag_entry = tk.Text(
            self.tab1, width=50, height=20, background=self.bgColor, foreground="black")
        self.hashtag_entry.grid(row=2, column=4, pady=40)

        # Buttons
        self.add_btn = tk.Button(self.tab1, text="Add User", width=12, foreground="white", background="blue")
        self.add_btn['command'] = self.add_user
        self.add_btn.grid(row=4, column=0, pady=30, padx=5)

        self.start_btn = tk.Button(self.tab1, text="Start Commenting", width=20, foreground="white", background="green")
        self.start_btn['command'] = Scraper
        self.start_btn.grid(row=4, column=1, pady=30, padx=5)

        self.contact_btn = tk.Label(self.tab1, text="For Any Issue Contact \n Click Here", width=30, foreground="red", cursor="hand2", background=self.bgColor)
        self.contact_btn.grid(row=4, column=3, pady=30, padx=5)
        self.contact_btn.bind("<Button-1>", self.contact)

        self.quit_btn = tk.Button(self.tab1, text="Exit", width=12, foreground="white", background="red")
        self.quit_btn['command'] = self.master.quit
        self.quit_btn.grid(row=4, column=4, pady=30, padx=5)


        #User Tab

        #buttons
        self.remove_btn = tk.Button(self.tab2, text="Remove User", width=12, command=self.remove_item)
        self.remove_btn.grid(row=0, column=0, pady=10, padx=5, sticky=tk.W)

        self.quit_btn = tk.Button(self.tab2, text="Exit", width=12, foreground="white", background="red")
        self.quit_btn['command'] = self.master.quit
        self.quit_btn.grid(row=0, column=1, pady=10, padx=5, sticky=tk.W)

        # users list (listbox)
        self.users_list_label = tk.Label(self.tab2, text='Users List', font=('bold', 20), pady=10, padx=5, background=self.bgColor, foreground="black")
        self.users_list_label.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)

        self.users_list = tk.Listbox(self.tab2, border=1, width=150, height=10, background=self.bgColor, foreground="black")
        self.users_list.grid(row=2, column=0, columnspan=3, rowspan=6, pady=5, padx=5, sticky=tk.W)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.tab2)
        self.scrollbar.grid(row=2, column=3)
        # Set scrollbar to users
        self.users_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.users_list.yview)

        self.users_list.bind('<<ListboxSelect>>', self.select_item)

    #contact event
    def contact(self, event):
        print(event)
        webbrowser.open_new("https://join.skype.com/invite/rM0hTYMK5chN")

    #populate users list
    def populate_list(self):
        
        self.users_list.delete(0, tk.END)

        rows = db.fetch()
        for row in rows:
            self.users_list.insert(tk.END, row)        
        
    
    # Add new User
    def add_user(self):
        if self.part_text.get() == '' or self.customer_text.get() == '' or self.conPass_text.get() == '' or self.retailer_text.get() == '' or self.comment_entry.get(1.0, "end-1c") == '' or self.hashtag_entry.get(1.0, "end-1c") == '':
            messagebox.showerror("Required Fields", "Please include all fields")
            return
        
        if self.conPass_text.get() != self.retailer_text.get():
            messagebox.showerror("Password Confirm Error", "Passwords not matched")
            return
        
        # Insert into DB
        db.createUser(
                self.part_text.get(), 
                self.customer_text.get(),
                self.retailer_text.get(), 
                self.comment_entry.get(1.0, "end-1c"), 
                self.hashtag_entry.get(1.0, "end-1c")
            )
        
        self.clear_text()
        self.populate_list()
        
        messagebox.showinfo("User Added", "Successfully User Added")
        return

    def select_item(self, event):
        try:
            index = self.users_list.curselection()[0]
            self.selected_item = self.users_list.get(index)
        except:
            pass

    def remove_item(self):
        try:
            db.remove(self.selected_item[0])
            self.clear_text()
            self.populate_list()
        except:
            messagebox.showinfo("Select", "Please Select an User")

    def clear_text(self):
        self.part_entry.delete(0, tk.END)
        self.customer_entry.delete(0, tk.END)
        self.retailer_entry.delete(0, tk.END)
        self.conPass_entry.delete(0, tk.END)
        self.conPass_entry.delete(0, tk.END)
        self.comment_entry.delete('1.0', tk.END)
        self.hashtag_entry.delete('1.0', tk.END)

root = tk.Tk()
app = Application(master=root)
app.mainloop()