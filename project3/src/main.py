from database.database import Database
from gui.app import App


if __name__ == '__main__':
    db = Database()
    db.connect()
    db.use_schema("test")

    app = App(db)
    app.mainloop()

    input()
    db.disconnect()
