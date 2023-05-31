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
            self.cursor.close()

    def manager_login(self, username: str, password: str) -> bool:
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(
                f"SELECT * FROM database_manager WHERE username = '{username}' AND password = '{password}'")
            result = self.cursor.fetchone()
            if result:
                print("Login Successful")
                self.manager = username
                self.director = None
                self.audience = None
                return True
            else:
                print("Login Failed")
                return False
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        finally:
            self.cursor.close()

    def director_login(self, username: str, password: str) -> bool:
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(f"SELECT * FROM director, user WHERE director.username = '{username}' AND \
                director.username = user.username AND user.password = '{password}'")
            result = self.cursor.fetchone()
            print(result)
            if result:
                print("Login Successful")
                self.director = username
                self.manager = None
                self.audience = None
                return True
            else:
                print("Login Failed")
                return False
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        finally:
            self.cursor.close()

    def audience_login(self, username: str, password: str) -> bool:
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(f"SELECT * FROM audience, user WHERE audience.username = '{username}' AND \
                audience.username = user.username AND user.password = '{password}'")
            result = self.cursor.fetchone()
            if result:
                print("Login Successful")
                self.audience = username
                self.manager = None
                self.director = None
                return True
            else:
                print("Login Failed")
                return False
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
        finally:
            self.cursor.close()

    def create_audience(self, username: str, password: str, name: str, surname: str) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(f"INSERT INTO user VALUES ('{username}', '{password}', '{name}', '{surname}')")
            self.cursor.execute(f"INSERT INTO audience VALUES ('{username}')")
            self.connection.commit()
            return "Audience created"
        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def create_director(self, username: str, password: str, name: str, surname: str, nation: str):
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(f"SELECT id FROM nation WHERE name = '{nation}'")
            if self.cursor.rowcount == 0:
                # add the nation to the nation table
                self.cursor.execute(f"INSERT INTO nation (name) VALUES ('{nation}')")
                self.connection.commit()
                self.cursor.execute(f"SELECT id FROM nation WHERE name = '{nation}'")
            nation_id = self.cursor.fetchone()[0]
            self.cursor.execute(f"INSERT INTO user VALUES ('{username}', '{password}', '{name}', '{surname}')")
            self.cursor.execute(f"INSERT INTO director VALUES ('{username}', {nation_id})")
            self.connection.commit()
            return "Director created"
        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def delete_audience(self, username: str) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(f"SELECT * FROM audience WHERE username = '{username}'")
            if self.cursor.rowcount == 0:
                return "Audience not found"
            self.cursor.execute(f"DELETE FROM audience WHERE username = '{username}'")
            self.cursor.execute(f"DELETE FROM user WHERE username = '{username}'")
            self.connection.commit()
            return "Audience deleted"
        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def update_director_platform(self, username: str, new_platform_id: str) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(f"SELECT * FROM director_platform WHERE director_username = '{username}'")
            if self.cursor.rowcount == 0:
                self.cursor.execute(f"INSERT INTO director_platform VALUES ('{username}', {new_platform_id})")
                return "Director updated"
            old_platform_id = self.cursor.fetchone()[1]
            self.cursor.execute(
                f"UPDATE director_platform SET platform_id = {new_platform_id} WHERE director_username = '{username}'")
            self.connection.commit()
            return "Director updated, old platform id: " + str(old_platform_id)
        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def read_directors(self) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(
                f"SELECT u.username, u.password, u.name, u.surname, n.name, dp.platform_id FROM user u JOIN director d ON d.username = u.username JOIN nation n ON n.id = d.nation_id LEFT OUTER JOIN director_platform dp ON u.username = dp.director_username")
            if self.cursor.rowcount == 0:
                return "No directors found"
            directors = "(username, name, surname, nation, platform-id)\n"
            for director in self.cursor.fetchall():
                directors += str(director) + "\n"
            return directors

        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def read_audience_ratings(self, username: str) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")  # movie id movie name rating
            self.cursor.execute(
                f"SELECT r.movie_id, m.name, r.rating FROM rating r JOIN movie m ON m.id = r.movie_id WHERE r.audience_username = '{username}'")
            if self.cursor.rowcount == 0:
                return "No ratings found"

            ratings = "(movie-id, movie-name, rating)\n"
            for rating in self.cursor.fetchall():
                ratings += str(rating) + "\n"
            return ratings

        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def read_director_movies(self, username: str) -> str:
        try:
            self.cursor = self.connection.cursor(
                buffered=True)  # movie id, movie name, theatre id, district, time slot.
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(
                f"SELECT m.id, m.name, t.id, t.district, ms.time_slot FROM movie_session ms JOIN movie m ON m.id = ms.movie_id JOIN theater t ON t.id = ms.theater_id WHERE m.director_username = '{username}'")
            if self.cursor.rowcount == 0:
                return "No movies found"

            movies = "(movie-id, movie-name, theatre-id, district, time-slot)\n"
            for movie in self.cursor.fetchall():
                movies += str(movie) + "\n"
            return movies

        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def read_movie_average_rating(self, movie_id: str) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")  # movie id movie name rating
            # self.cursor.execute(f"SELECT AVG(rating) FROM rating WHERE movie_id = {movie_id}")
            self.cursor.execute(f"SELECT m.average_rating FROM movie m WHERE m.id = {movie_id}")
            if self.cursor.rowcount == 0:
                return "No movie found"
            return str(self.cursor.fetchone()[0])

        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def execute_manager_query(self, query: str) -> str:
        # get the tokens from the query string
        tokens = [token.lower() if i < 2 else token for i, token in enumerate(query.split())]
        # check if the query is valid
        if len(tokens) < 2:
            return "Invalid query"

        if tokens[0] not in ["create", "delete", "update", "read"]:
            return "Invalid query"

        if tokens[0] == "create":
            if tokens[1] == "audience":
                if len(tokens) != 6:
                    return "Invalid query"

                return self.create_audience(tokens[2], tokens[3], tokens[4], tokens[5])
            elif tokens[1] == "director":
                if len(tokens) != 7:
                    return "Invalid query"

                return self.create_director(tokens[2], tokens[3], tokens[4], tokens[5], tokens[6])
            else:
                return "Invalid query"
        elif tokens[0] == "delete":
            if tokens[1] == "audience":
                if len(tokens) != 3:
                    return "Invalid query"

                return self.delete_audience(tokens[2])
            else:
                return "Invalid query"

        elif tokens[0] == "update":
            if tokens[1] == "director-platform":
                if len(tokens) != 4:
                    return "Invalid query"

                return self.update_director_platform(tokens[2], tokens[3])
            else:
                return "Invalid query"

        elif tokens[0] == "read":
            if tokens[1] == "directors":
                if len(tokens) != 2:
                    return "Invalid query"

                return self.read_directors()
            elif tokens[1] == "audience-ratings":
                if len(tokens) != 3:
                    return "Invalid query"

                return self.read_audience_ratings(tokens[2])
            elif tokens[1] == "director-movies":
                if len(tokens) != 3:
                    return "Invalid query"

                return self.read_director_movies(tokens[2])
            elif tokens[1] == "movie-average-rating":
                if len(tokens) != 3:
                    return "Invalid query"

                return self.read_movie_average_rating(tokens[2])
            else:
                return "Invalid query"

    def create_movie(self, movie_id: str, movie_name: str, theater_id: str, time_slot: str) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(f"SELECT * FROM movie WHERE id = {movie_id}")
            if int(time_slot) < 0 or int(time_slot) > 4:
                return "Invalid time slot"
            if self.cursor.rowcount == 0:
                self.cursor.execute(
                    f"INSERT INTO movie (id, name, director_username) VALUES ({movie_id}, '{movie_name}', '{self.director}')")
            self.cursor.execute(
                f"INSERT INTO movie_session (movie_id, theater_id, time_slot) VALUES ({movie_id}, {theater_id}, '{time_slot}')")
            self.connection.commit()
            return "Movie created"

        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def update_predecessor(self, movie_id: str, predecessor_id: list[str]) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            for id in predecessor_id:
                self.cursor.execute(
                    f"INSERT INTO movie_predecessor (movie_id, predecessor_id) VALUES ({movie_id}, {id})")
            self.connection.commit()
            return "Predecessor updated"

        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def update_movie(self, movie_id: str, movie_name: str) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(f"UPDATE movie SET name = '{movie_name}' WHERE id = {movie_id}")
            self.connection.commit()
            return "Movie updated"

        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def read_movies(self) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(
                f"SELECT DISTINCT m.id, m.name, ms.theater_id, ms.time_slot FROM movie m, movie_session ms WHERE m.id = ms.movie_id AND m.director_username = '{self.director}' ORDER BY m.id")
            if self.cursor.rowcount == 0:
                return "No movies found"
            result = self.cursor.fetchall()
            for i in range(len(result)):
                self.cursor.execute(f"SELECT predecessor_id FROM movie_predecessor WHERE movie_id = {result[i][0]}")
                if self.cursor.rowcount == 0:
                    result[i] = result[i] + ("None",)
                else:
                    predecessors = self.cursor.fetchall()
                    predecessors_list = []
                    for predecessor in predecessors:
                        predecessors_list.append(str(predecessor[0]))
                    result[i] = result[i] + (", ".join(predecessors_list),)
            movie_list = ["movie_id, movie_name, theatre_id, time_slot", "predecessors"]
            for i, row in enumerate(result):
                movie_list.append(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}")
            return "\n".join(movie_list)

        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def read_audiences(self, movie_id: str) -> str:
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(f"USE {self.default_schema}")
            self.cursor.execute(
                f"SELECT a.username, a.name, a.surname FROM audience a, movie_audience ma WHERE a.username = ma.audience_username AND ma.movie_id = {movie_id}")
            if self.cursor.rowcount == 0:
                return "No audiences found"
            result = self.cursor.fetchall()
            audience_list = ["username, name, surname"]
            for row in result:
                audience_list.append(f"{row[0]} {row[1]} {row[2]}")
            return "\n".join(audience_list)

        except mysql.connector.Error as err:
            return f"Error: '{err}'"
        finally:
            self.cursor.close()

    def execute_director_query(self, query: str) -> str:
        tokens = [token.lower() if i < 2 else token for i, token in enumerate(query.split())]
        # check if the query is valid
        if len(tokens) < 2:
            return "Invalid query"

        if tokens[0] not in ["create", "delete", "update", "read"]:
            return "Invalid query"

        if tokens[0] == "create":
            if tokens[1] == "movie":
                if len(tokens) != 6:
                    return "Invalid query"

                return self.create_movie(tokens[2], tokens[3], tokens[4], tokens[5])
            else:
                return "Invalid query"
        elif tokens[0] == "update":
            if tokens[1] == "predecessor":
                if len(tokens) < 4:
                    return "Invalid query"

                return self.update_predecessor(tokens[2], tokens[3:])
            elif tokens[1] == "movie":
                if len(tokens) != 4:
                    return "Invalid query"

                return self.update_movie(tokens[2], tokens[3])
            else:
                return "Invalid query"
        elif tokens[0] == "read":
            if tokens[1] == "movies":
                if len(tokens) != 2:
                    return "Invalid query"

                return self.read_movies()
            elif tokens[1] == "audiences":
                if len(tokens) != 3:
                    return "Invalid query"

                return self.read_audiences(tokens[2])
            elif tokens[1] == "theaters": # read theaters <slot>
                if len(tokens) != 3:
                    return "Invalid query"

                return self.read_theaters(tokens[2])
            else:
                return "Invalid query"
        else:
            return "Invalid query"

    def execute_audience_query(self, query: str):
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

