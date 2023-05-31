import tkinter as tk
from tkinter import ttk

from database.database import Database


class App(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self.database = db
        self.manager_login = False
        self.audience_login = False
        self.director_login = False

        # Set window title and size
        self.title("Database Management System")
        self.geometry("800x600")

        # Create a login screen
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(expand=1, fill="both")

        # Create a label and combobox for role selection
        self.role_label = ttk.Label(self.login_frame, text="Select a role:")
        self.role_label.pack(pady=10)

        self.role_var = tk.StringVar()
        self.role_combobox = ttk.Combobox(self.login_frame, textvariable=self.role_var,
                                          values=["Database Manager", "Director", "Audience"])
        self.role_combobox.pack()

        # Create a frame for Manager/Director login
        self.login_frame_fields = ttk.Frame(self.login_frame)
        self.login_frame_fields.pack(pady=10)

        # Create entry fields for username and password
        self.username_label = ttk.Label(self.login_frame_fields, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.login_frame_fields)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = ttk.Label(self.login_frame_fields, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.login_frame_fields, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create a login button
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        # Create a Pane for each role
        self.panes = ttk.PanedWindow(self, orient="vertical")
        self.panes.pack(expand=1, fill="both")

        # Create widgets for the Manager pane
        self.manager_pane = ttk.Frame(self.panes)
        self.manager_label = ttk.Label(self.manager_pane, text="Manager")
        self.manager_label.pack(pady=10)

        # Create widgets for the Director pane
        self.director_pane = ttk.Frame(self.panes)
        self.director_label = ttk.Label(self.director_pane, text="Director")
        self.director_label.pack(pady=10)

        # Create widgets for the Audience pane
        self.audience_pane = ttk.Frame(self.panes)
        self.audience_label = ttk.Label(self.audience_pane, text="Audience")
        self.audience_label.pack(pady=10)

    def login(self):
        # Get the selected role
        role = self.role_var.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check the role and perform appropriate login action
        if role == "Database Manager":
            self.manager_login = self.database.manager_login(username, password)
            if self.manager_login:
                self.login_frame.pack_forget()
                self.manager_frame.pack(expand=1, fill="both")

        elif role == "Director":
            self.director_login = self.database.director_login(username, password)
            if self.director_login:
                self.login_frame.pack_forget()
                self.director_frame.pack(expand=1, fill="both")

        elif role == "Audience":
            self.audience_login = self.database.audience_login(username, password)
            if self.audience_login:
                self.login_frame.pack_forget()
                self.audience_frame.pack(expand=1, fill="both")


if __name__ == '__main__':
    app = App()
    app.mainloop()
