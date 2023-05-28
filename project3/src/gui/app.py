import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

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
                                          values=["Manager", "Director", "Audience"])
        self.role_combobox.pack()

        # Create a frame for Manager/Director login
        self.login_frame2 = ttk.Frame(self.login_frame)
        self.login_frame2.pack(pady=10)

        # Create entry fields for username and password
        self.username_label = ttk.Label(self.login_frame2, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.login_frame2)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = ttk.Label(self.login_frame2, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.login_frame2, show="*")
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

        # Check the role and perform appropriate login action
        if role == "Manager":
            username = self.username_entry.get()
            password = self.password_entry.get()
            if username == "admin" and password == "password":
                # Login successful, show Manager pane
                self.panes.add(self.manager_pane, text="Manager")
                self.panes.show(self.manager_pane)
        elif role == "Director":
            username = self.username_entry.get()
            password = self.password_entry.get()
            if username == "director" and password == "password":
                # Login successful, show Director pane
                self.panes.add(self.director_pane, text="Director")
                self.panes.show(self.director_pane)
        elif role == "Audience":
            confirmation = tk.messagebox.askyesno("Confirmation", "Do you want to log in as an Audience?")
            if confirmation:
                # Login successful, show Audience pane
                self.panes.add(self.audience_pane, text="Audience")
                self.panes.show(self.audience_pane)

    def add_user(self):
        # TODO: Implement adding a new user to the system
        pass

    def delete_audience(self):
        # TODO: Implement deleting an audience and all related data from the system
        pass

    def update_director_platform(self):
        # TODO: Implement updating the platform id of a director
        pass

    def view_directors(self):
        # TODO: Implement viewing all directors and their attributes
        pass

    def view_audience_ratings(self):
        # TODO: Implement viewing all ratings of a specific audience
        pass

    def view_director_movies(self):
        # TODO: Implement viewing all movies of a specific director
        pass

    def view_movie_rating(self):
        # TODO: Implement viewing the average rating of a movie
        pass

    def list_theatres_for_slot(self):
        # TODO: Implement listing all theatres available for a given slot
        pass

    def add_movie(self):
        # TODO: Implement adding a new movie to the system
        pass

    def add_predecessor(self):
        # TODO: Implement adding predecessor(s) to a movie
        pass

    def view_director_movies(self):
        # TODO: Implement viewing all movies directed by a director in ascending order of movie id
        pass

    def view_audience_for_movie(self):
        # TODO: Implement viewing all audiences who bought a ticket for a specific movie directed by a director
        pass

    def update_movie_name(self):
        # TODO: Implement updating the name of a movie directed by a director
        pass

    def list_all_movies(self):
        # TODO: Implement listing all movies and their attributes for an audience
        pass

    def buy_movie_ticket(self):
        # TODO: Implement buying a movie ticket for an audience
        pass

    def view_tickets(self):
        # TODO: Implement viewing all tickets bought by an audience
        pass

if __name__ == '__main__':
    app = App()
    app.mainloop()
