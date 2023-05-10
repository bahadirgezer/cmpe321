import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("My App")
        self.geometry("600x400")

        # Create a tab control
        self.tabControl = ttk.Notebook(self)

        # Create tabs
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)

        # Add tabs to the tab control
        self.tabControl.add(self.tab1, text='Tab 1')
        self.tabControl.add(self.tab2, text='Tab 2')

        # Create a label and button in the first tab
        self.label1 = ttk.Label(self.tab1, text='Hello, world!')
        self.label1.pack(padx=10, pady=10)

        self.button1 = ttk.Button(self.tab1, text='Click me!', command=self.button_clicked)
        self.button1.pack(padx=10, pady=10)

        # Create an entry field and button in the second tab
        self.entry2 = ttk.Entry(self.tab2)
        self.entry2.pack(padx=10, pady=10)

        self.button2 = ttk.Button(self.tab2, text='Print text', command=self.print_text)
        self.button2.pack(padx=10, pady=10)

        # Pack the tab control
        self.tabControl.pack(expand=1, fill="both")

    # Event handler for the button in tab 1
    def button_clicked(self):
        self.label1.config(text='Button clicked!')

    # Event handler for the button in tab 2
    def print_text(self):
        text = self.entry2.get()
        print(text)

    def run(self):
        self.mainloop()


def my_window():
    # create a small window to display the results with tkinter
    root = tk.Tk()
    root.title("MySQL")
    root.geometry("500x500")
    root.configure(bg="white")
    root.resizable(False, False)

    # create a label to display the results
    label = tk.Label(root, text="MySQL", bg="white", font=("Arial", 20))
    label.pack(pady=20)

    # create a frame to hold the buttons
    button_frame = tk.Frame(root, bg="white")
    button_frame.pack()

    # create the schema name entry
    schema_name_entry = tk.Entry(button_frame, font=("Arial", 20), justify="center")
    schema_name_entry.pack(pady=20)

    database_name_entry = tk.Entry(button_frame, font=("Arial", 20), justify="center")
    database_name_entry.pack(pady=20)

    # create the buttons

    # create a button to create a schema
    create_schema_button = tk.Button(button_frame, text="Create Schema", font=("Arial", 20), padx=10, pady=10,
                                     command=lambda: db.create_schema(schema_name_entry.get()))

    create_schema_button.pack(pady=20)

    create_table_button = tk.Button(button_frame, text="Create Table", font=("Arial", 20), padx=10, pady=10,
                                    command=lambda: db.create_table(schema_name_entry.get(), database_name_entry.get()))

    create_table_button.pack(pady=20)

    # run the window
    root.mainloop()