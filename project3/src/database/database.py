import os
import mysql.connector


class Database:
    def __init__(self):
        self.director = None
        self.manager = None
        self.audience = None
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

    def create_table(self, table_name: str, schema_name: str = None, columns: list[str] = None):
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
            self.cursor.close()    def execute_audience_query(self, query: str):
        # get the tokens from the query string
        tokens = [token.lower() if i < 2 else token for i, token in enumerate(query.split())]
        # check if the query is valid
        if len(tokens) < 2:
            return "Invalid query"

        if tokens[0] not in ["create", "read"]:
            return "Invalid query"

        if tokens[0] == "create":
            if tokens[1] == "ticket":
                if len(tokens) != 3:
                    return "Invalid query"

                return self.create_ticket(tokens[2])
            else:
                return "Invalid query"
        elif tokens[0] == "read":
            if tokens[1] == "tickets":
                if len(tokens) != 2:
                    return "Invalid query"

                return self.read_tickets()
            elif tokens[1] == "movies":
                if len(tokens) != 2:
                    return "Invalid query"

                return self.read_movies_audience()
            else:
                return "Invalid query"
        else:
            return "Invalid query"

