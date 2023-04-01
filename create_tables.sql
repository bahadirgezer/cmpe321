CREATE TABLE Audience(
username VARCHAR(255), 
password VARCHAR(255) NOT NULL,
name VARCHAR(255),
surname VARCHAR(255),
PRIMARY KEY (username)
);

CREATE TABLE Director(
username VARCHAR(255), 
password VARCHAR(255) NOT NULL,
name VARCHAR(255),
surname VARCHAR(255),
nation VARCHAR(255) NOT NULL,
platform _id INT,
PRIMARY KEY (username),
FOREIGN KEY (platform_id) REFERENCES Rating_Platform
	ON DELETE SET NULL
ON UPDATE CASCADE
);

CREATE TABLE Rating_Platform(
id INT, 
name VARCHAR(255) UNIQUE,
PRIMARY KEY (id)
);

CREATE TABLE Movie(
id INT, 
name VARCHAR(255),
duration INT,
overall_rating REAL,
director_name VARCHAR(255) NOT NULL, 
PRIMARY KEY (id),
FOREIGN KEY (director_name) REFERENCES Director
	ON DELETE CASCADE
ON UPDATE CASCADE
); 

CREATE TABLE Movie_Session(
id INT, 
movie_id INT NOT NULL,
theater_id INT NOT NULL,
time_slot INT NOT NULL,
date DATE NOT NULL, 
PRIMARY KEY (id),
FOREIGN KEY (movie_id) REFERENCES Movie
	ON DELETE SET NULL
	ON UPDATE CASCADE,
FOREIGN KEY (theater_id) REFERENCES Theater
	ON DELETE SET NULL
	ON UPDATE CASCADE
);

CREATE TABLE Theater
(
id INT, 
name VARCHAR(255),
capacity INT,
district VARCHAR(255),
PRIMARY KEY (id)
);

CREATE TABLE Genre(
	id INT,
	name VARCHAR(255) UNIQUE
	PRIMARY KEY (id)
);

CREATE TABLE Ticket(
username VARCHAR(255), 
session_id INT,,
PRIMARY KEY (username, session_id),
FOREIGN KEY (username) REFERENCES Audience
	ON DELETE SET NULL
	ON UPDATE CASCADE,,
FOREIGN KEY (session_id) REFERENCES Movie_Session
	ON DELETE SET NULL
	ON UPDATE CASCADE,
);

CREATE TABLE Platform_Subscription(
username VARCHAR(255), 
platform_id INT,,
PRIMARY KEY (username, platform_id),
FOREIGN KEY (username) REFERENCES Audience
	ON DELETE CASCADE
	ON UPDATE CASCADE,
FOREIGN KEY (platform_id) REFERENCES Rating_Platform
	ON DELETE CASCADE
	ON UPDATE CASCADE
);


CREATE TABLE Movie_Ratings(
username VARCHAR(255), 
movie_id INT,
rating REAL,
PRIMARY KEY (username, movie_id),
FOREIGN KEY (username) REFERENCES Audience,
ON DELETE SET NULL
	ON UPDATE CASCADE
FOREIGN KEY (movie_id) REFERENCES Movie
ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE Movie_Genre(
movie_id INT,
genre_id INT,
PRIMARY KEY (movie_id, genre_id),
FOREIGN KEY (movie_id) REFERENCES Movie,
ON DELETE CASCADE
	ON UPDATE CASCADE
FOREIGN KEY (genre_id) REFERENCES Genre
ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE Movie_Predecessor(
predecessor_id INT,
successor_id INT,
PRIMARY KEY (predecessor_id, successor_id),
FOREIGN KEY (predecessor_id) REFERENCES Movie,
ON DELETE CASCADE
	ON UPDATE CASCADE
FOREIGN KEY (successor_id) REFERENCES Movie
ON DELETE CASCADE
	ON UPDATE CASCADE
);
 

CREATE TABLE Database_Managers(
username VARCHAR(255), 
password VARCHAR(255),
PRIMARY KEY (username)
);



