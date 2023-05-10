import os
import mysql.connector


class Column:
    def __init__(self,
                 name: str = None,
                 data_type: str = None,
                 length: int = None,  # for varchar
                 precision: int = None,  # for decimal
                 scale: int = None,  # for decimal
                 nullable: bool = None,
                 primary_key: bool = None,
                 auto_increment: bool = None,
                 default: str = None,
                 unique: bool = None,
                 check: str = None,  # for check constraint
                 foreign_key: str = None,  # for foreign key constraint
                 reference: str = None,  # for foreign key constraint
                 on_update: str = None,  # for foreign key constraint
                 on_delete: str = None,  # for foreign key constraint
                 index: bool = None,
                 index_name: str = None,
                 index_type: str = None,
                 index_columns: list = None):

        self.name = name
        self.data_type = data_type
        self.length = length
        self.precision = precision
        self.scale = scale
        self.nullable = nullable
        self.primary_key = primary_key
        self.auto_increment = auto_increment
        self.default = default
        self.unique = unique
        self.check = check
        self.foreign_key = foreign_key
        self.reference = reference
        self.on_update = on_update
        self.on_delete = on_delete
        self.index = index
        self.index_name = index_name
        self.index_type = index_type
        self.index_columns = index_columns

    def __str__(self):
        # return the column create table statement
        column = f"{self.name} {self.data_type}"
        if self.length:
            column += f"({self.length})"
        if self.precision:
            column += f"({self.precision},{self.scale})"
        if not self.nullable:
            column += " NOT NULL"
        if self.primary_key:
            column += " PRIMARY KEY"
        if self.auto_increment:
            column += " AUTO_INCREMENT"
        if self.default:
            column += f" DEFAULT {self.default}"
        if self.unique:
            column += " UNIQUE"
        if self.check:
            column += f" CHECK ({self.check})"
        if self.foreign_key:
            column += f" FOREIGN KEY ({self.foreign_key})"
            column += f" REFERENCES {self.reference}"
            if self.on_update:
                column += f" ON UPDATE {self.on_update}"
            if self.on_delete:
                column += f" ON DELETE {self.on_delete}"
        return column



class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.default_schema = ""

    def connect(self,
                user_password: str = os.getenv("MYSQL_ROOT_PASSWORD"),
                host_name: str = "localhost",
                user_name: str = "root"):

        try:
            self.connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                password=user_password,
            )
            print("MySQL: connected to {}...".format(self.connection.get_server_info()))
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")

        return self.connection

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("MySQL: connection closed.")

    def create_schema(self, schema_name: str):
        try:
            self.cursor = self.connection.cursor()
            # check if the schema exists
            self.cursor.execute(f"SHOW DATABASES LIKE '{schema_name}'")
            result = self.cursor.fetchone()
            if result:
                print(f"MySQL: schema '{schema_name}' already exists.")
                return
            # create the schema
            self.cursor.execute(f"CREATE DATABASE {schema_name}")
            print(f"MySQL: schema '{schema_name}' created.")
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        finally:
            self.cursor.close()

    def delete_schema(self, schema_name: str = None):
        schema_name = schema_name if schema_name else self.default_schema
        try:
            self.cursor = self.connection.cursor()
            # check if the schema exists
            self.cursor.execute(f"SHOW DATABASES LIKE '{schema_name}'")
            result = self.cursor.fetchone()
            if not result:
                print(f"MySQL: schema '{schema_name}' does not exist.")
                return

            # delete the schema
            self.cursor.execute(f"USE {schema_name}")
            self.cursor.execute("SHOW TABLES")
            result = self.cursor.fetchall()
            if result:
                print(f"MySQL: schema '{schema_name}' has tables in it.")
                while True:
                    delete_tables = input("Do you want to delete the tables? (y/n) ").lower()
                    if delete_tables == "y":
                        for table in result:
                            self.cursor.execute(f"DROP TABLE {table[0]}")
                        self.cursor.execute(f"DROP DATABASE {schema_name}")
                    elif delete_tables == "n":
                        print(f"MySQL: schema '{schema_name}' not deleted.")
                        return
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        finally:
            print(f"MySQL: schema '{schema_name}' deleted.")
            self.cursor.close()

    def create_table(self, table_name: str, schema_name: str = None, columns: list[Column] = None):
        schema_name = schema_name if schema_name else self.default_schema
        try:
            self.cursor = self.connection.cursor()
            # check if the schema exists
            self.cursor.execute(f"SHOW DATABASES LIKE '{schema_name}'")
            result = self.cursor.fetchone()
            if not result:
                print(f"MySQL: schema '{schema_name}' does not exist.")
                return

            # check if the table exists
            self.cursor.execute(f"USE {schema_name}")
            self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = self.cursor.fetchone()
            if result:
                print(f"MySQL: table '{table_name}' already exists.")
                return

            # create the table
            # create the columns
            columns_str = ""
            for column in columns:
                columns_str += f"{column}, "
            columns_str = columns_str[:-2]
            # create the table
            self.cursor.execute(f"CREATE TABLE {table_name} ({columns_str})")
            print(f"MySQL: table '{table_name}' created.")
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        finally:
            self.cursor.close()

    def delete_table(self, table_name: str, schema_name: str = None):
        schema_name = schema_name if schema_name else self.default_schema
        try:
            self.cursor = self.connection.cursor()
            # check if the schema exists
            self.cursor.execute(f"SHOW DATABASES LIKE '{schema_name}'")
            result = self.cursor.fetchone()
            if not result:
                print(f"MySQL: schema '{schema_name}' does not exist.")
                return

            # check if the table exists
            self.cursor.execute(f"USE {schema_name}")
            self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = self.cursor.fetchone()
            if not result:
                print(f"MySQL: table '{table_name}' does not exist.")
                return

            # delete the table
            self.cursor.execute(f"DROP TABLE {table_name}")
            print(f"MySQL: table '{table_name}' deleted.")
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        finally:
            self.cursor.close()

    def use_schema(self, schema: str):
        if schema is None:
            self.default_schema = ""
            return
        # check if the schema exists
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SHOW DATABASES LIKE '{schema}'")
        result = self.cursor.fetchone()
        if not result:
            print(f"MySQL: schema '{schema}' does not exist.")
            return
        self.default_schema = schema
        print(f"MySQL: using schema '{schema}'")
        self.cursor.close()

    def get_schema(self):
        return self.default_schema

    def execute_query(self, query: str):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        finally:
            self.cursor.close()