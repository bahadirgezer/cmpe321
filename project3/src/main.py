import database.query as q
from database.database import Database
import tkinter as tk


def mywindow():
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


if __name__ == '__main__':
    db = Database()
    db.connect()

    input()
    db.disconnect()
