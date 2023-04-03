CREATE TABLE Audience (
    username VARCHAR(255),
    password VARCHAR(255) NOT NULL, -- every user requires a password
    name VARCHAR(255),
    surname VARCHAR(255),
    PRIMARY KEY (username)
);
CREATE TABLE Genre (
    id INT,
    name VARCHAR(255) UNIQUE, -- from description
    PRIMARY KEY (id)
);
CREATE TABLE Database_Managers (
    username VARCHAR(255),
    password VARCHAR(255),
    PRIMARY KEY (username)
);
CREATE TABLE Rating_Platform (
    id INT,
    name VARCHAR(255) UNIQUE, -- from description
    PRIMARY KEY (id)
);
CREATE TABLE Theater (
    id INT,
    name VARCHAR(255),
    capacity INT,
    district VARCHAR(255),
    PRIMARY KEY (id)
);
CREATE TABLE Director (
    username VARCHAR(255),
    password VARCHAR(255) NOT NULL, -- every user requires a password
    name VARCHAR(255),
    surname VARCHAR(255),
    nation VARCHAR(255) NOT NULL, -- every director must have only one nation
    platform_id INT,
    PRIMARY KEY (username),
    FOREIGN KEY (platform_id)
        REFERENCES Rating_Platform (id)
        ON DELETE SET NULL ON UPDATE CASCADE -- director *can* have a platform
);
CREATE TABLE Movie (
    id INT,
    name VARCHAR(255),
    duration INT,
    overall_rating REAL,
    director_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (director_name)
        REFERENCES Director (username)
        ON DELETE CASCADE ON UPDATE CASCADE -- every movie requires a director
);
CREATE TABLE Movie_Session (
    id INT,
    movie_id INT NOT NULL,
    theater_id INT NOT NULL,
    time_slot INT NOT NULL, -- movie sessions must have a time and date
    date DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (movie_id)
        REFERENCES Movie (id)
        ON DELETE CASCADE ON UPDATE CASCADE, -- every movie session requires a movie
    FOREIGN KEY (theater_id)
        REFERENCES Theater (id)
        ON DELETE CASCADE ON UPDATE CASCADE -- every movie session requires a theater
);
CREATE TABLE Ticket (
    username VARCHAR(255),
    session_id INT,
    PRIMARY KEY (username , session_id),
    FOREIGN KEY (username)
        REFERENCES Audience (username)
        ON DELETE CASCADE ON UPDATE CASCADE, -- every ticket must have an audience
    FOREIGN KEY (session_id)
        REFERENCES Movie_Session (id)
        ON DELETE CASCADE ON UPDATE CASCADE -- every ticket must have a movie session 
);
CREATE TABLE Platform_Subscription (
    username VARCHAR(255),
    platform_id INT,
    PRIMARY KEY (username , platform_id),
    FOREIGN KEY (username)
        REFERENCES Audience (username)
        ON DELETE CASCADE ON UPDATE CASCADE, -- every subscription must have an audience
    FOREIGN KEY (platform_id)
        REFERENCES Rating_Platform (id)
        ON DELETE CASCADE ON UPDATE CASCADE -- every subscription must be on a platform
);
CREATE TABLE Movie_Ratings (
    username VARCHAR(255),
    movie_id INT,
    rating REAL,
    PRIMARY KEY (username , movie_id),
    FOREIGN KEY (username)
        REFERENCES Audience (username)
        ON DELETE CASCADE ON UPDATE CASCADE, -- every rating must have an audience connected to it
    FOREIGN KEY (movie_id)
        REFERENCES Movie (id)
        ON DELETE CASCADE ON UPDATE CASCADE -- every rating requires a movie
);
CREATE TABLE Movie_Genre (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id , genre_id),
    FOREIGN KEY (movie_id)
        REFERENCES Movie (id)
        ON DELETE CASCADE ON UPDATE CASCADE, -- every genre-movie mapping must have both a genre and a movie
    FOREIGN KEY (genre_id)
        REFERENCES Genre (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE Movie_Predecessor (
    predecessor_id INT,
    successor_id INT,
    PRIMARY KEY (predecessor_id , successor_id),
    FOREIGN KEY (predecessor_id)
        REFERENCES Movie (id)
        ON DELETE CASCADE ON UPDATE CASCADE, -- every movie-movie mapping must have both movies 
    FOREIGN KEY (successor_id)
        REFERENCES Movie (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);