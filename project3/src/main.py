import database.query as q
from database.database import Database, Column
import tkinter as tk
from gui.app import App


def loop(db: Database):
    keyboard_input: str = ""
    while keyboard_input != "exit":
        print(db.execute_query(keyboard_input))
        keyboard_input = input("> ")
    db.disconnect()


if __name__ == '__main__':
    db = Database()
    db.connect()
    db.use_schema("movie")
    db.create_table("audience", columns=[
        Column(name="id", data_type="int", primary_key=True, auto_increment=True),
        Column(name="name", data_type="varchar", length=50),
        Column(name="age", data_type="int"),
        Column(name="username", data_type="varchar", length=50, unique=True),
    ])
    # App().run()
    loop(db)


    input()
    db.disconnect()
