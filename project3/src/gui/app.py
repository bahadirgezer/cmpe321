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

        # MANAGER FRAME
        # Create a Pane for each role
        # Create widgets for the Manager pane
        self.manager_frame = ttk.Frame(self)
        self.manager_label = ttk.Label(self.manager_frame, text="Database Manager")
        self.manager_label.pack(pady=10)
        # add text box for query, make the text box scrollable
        self.manager_query_text = tk.Text(self.manager_frame, height=10, width=50)
        self.manager_query_text.pack(pady=10)
        # submit
        self.manager_submit_button = ttk.Button(self.manager_frame, text="Submit", command=self.manager_submit)
        self.manager_submit_button.pack(pady=10)
        # add text box for response, make the text box scrollable
        self.manager_query_response = tk.Label(self.manager_frame, text="Query")
        self.manager_query_response.pack(pady=10)

        # DIRECTOR FRAME
        # Create widgets for the Director pane
        self.director_frame = ttk.Frame(self)
        self.director_label = ttk.Label(self.director_frame, text="Director")
        self.manager_label.pack(pady=10)
        self.director_query_text = tk.Text(self.director_frame, height=10, width=50)
        self.director_query_text.pack(pady=10)
        self.director_submit_button = ttk.Button(self.director_frame, text="Submit", command=self.director_submit)
        self.director_submit_button.pack(pady=10)
        self.director_query_response = tk.Label(self.director_frame, text="Query")
        self.director_query_response.pack(pady=10)

        # AUDIENCE FRAME
        # Create widgets for the Audience pane
        self.audience_frame = ttk.Frame(self)
        self.audience_label = ttk.Label(self.audience_frame, text="Audience")
        self.audience_label.pack(pady=10)
        self.audience_query_text = tk.Text(self.audience_frame, height=10, width=50)
        self.audience_query_text.pack(pady=10)
        self.audience_submit_button = ttk.Button(self.audience_frame, text="Submit", command=self.audience_submit)
        self.audience_submit_button.pack(pady=10)
        self.audience_query_response = tk.Label(self.audience_frame, text="Query")
        self.audience_query_response.pack(pady=10)

    def manager_submit(self):
        input: str = self.manager_query_text.get("1.0", "end-1c")
        self.manager_query_response["text"] = self.database.execute_manager_query(input)

    def director_submit(self):
        input: str = self.director_query_text.get("1.0", "end-1c")
        self.director_query_response["text"] = self.database.execute_director_query(input)

    def audience_submit(self):
        input: str = self.audience_query_text.get("1.0", "end-1c")
        self.audience_query_response["text"] = self.database.execute_audience_query(input)

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
