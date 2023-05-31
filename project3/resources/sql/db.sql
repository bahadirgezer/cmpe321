CREATE TABLE `nation` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `user` (
    `username` VARCHAR(45) NOT NULL,
    `password` VARCHAR(45) NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `surname` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`username`),
    UNIQUE KEY `username_UNIQUE` (`username`)
);

CREATE TABLE `audience` (
    `username` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`username`),
    CONSTRAINT `username` FOREIGN KEY (`username`)
        REFERENCES `user` (`username`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `database_manager` (
    `username` VARCHAR(45) NOT NULL,
    `password` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`username`)
);

CREATE TABLE `director` (
    `username` VARCHAR(45) NOT NULL,
    `nation_id` INT NOT NULL,
    PRIMARY KEY (`username`),
    KEY `nation_idx` (`nation_id`),
    CONSTRAINT `nation` FOREIGN KEY (`nation_id`)
        REFERENCES `nation` (`id`)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `user` FOREIGN KEY (`username`)
        REFERENCES `user` (`username`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `rating_platform` (
    `id` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`),
    UNIQUE KEY `name_UNIQUE` (`name`)
);

CREATE TABLE `director_platform` (
    `director_username` VARCHAR(45) NOT NULL,
    `platform_id` INT NOT NULL,
    PRIMARY KEY (`director_username`),
    UNIQUE KEY `username_UNIQUE` (`director_username`),
    KEY `rating_platform_idx` (`platform_id`),
    CONSTRAINT `director_on` FOREIGN KEY (`director_username`)
        REFERENCES `director` (`username`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `rating_platform` FOREIGN KEY (`platform_id`)
        REFERENCES `rating_platform` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `genre` (
    `id` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name_UNIQUE` (`name`),
    UNIQUE KEY `id_UNIQUE` (`id`)
);

CREATE TABLE `movie` (
    `id` INT NOT NULL,
    `average_rating` FLOAT NOT NULL DEFAULT '0',
    `name` VARCHAR(45) NOT NULL,
    `duration` INT NOT NULL DEFAULT '1',
    `director_username` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`),
    UNIQUE KEY `name_UNIQUE` (`name`),
    KEY `director_idx` (`director_username`),
    CONSTRAINT `director` FOREIGN KEY (`director_username`)
        REFERENCES `director` (`username`)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE `movie_genre` (
    `movie_id` INT NOT NULL,
    `genre_id` INT NOT NULL,
    PRIMARY KEY (`movie_id` , `genre_id`),
    KEY `genre_idx` (`genre_id`),
    CONSTRAINT `genre` FOREIGN KEY (`genre_id`)
        REFERENCES `genre` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `movie` FOREIGN KEY (`movie_id`)
        REFERENCES `movie` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `theater` (
    `id` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `capacity` INT NOT NULL,
    `district` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `movie_session` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `time_slot` INT NOT NULL,
    `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `movie_id` INT NOT NULL,
    `theater_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    KEY `theater_idx` (`theater_id`),
    KEY `movie_idx` (`movie_id`),
    CONSTRAINT `screenin` FOREIGN KEY (`movie_id`)
        REFERENCES `movie` (`id`)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `theater` FOREIGN KEY (`theater_id`)
        REFERENCES `theater` (`id`)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE `rating` (
    `movie_id` INT NOT NULL,
    `audience_username` VARCHAR(45) NOT NULL,
    `rating` FLOAT NOT NULL,
    PRIMARY KEY (`movie_id` , `audience_username`),
    UNIQUE KEY `audience_username_UNIQUE` (`audience_username`),
    CONSTRAINT `movie_rating` FOREIGN KEY (`movie_id`)
        REFERENCES `movie` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `audience_rating` FOREIGN KEY (`audience_username`)
        REFERENCES `audience` (`username`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `subscription` (
    `audience_username` VARCHAR(45) NOT NULL,
    `platform_id` INT NOT NULL,
    PRIMARY KEY (`audience_username` , `platform_id`),
    KEY `rating_platform_idx` (`platform_id`),
    CONSTRAINT `audience_subscribed` FOREIGN KEY (`audience_username`)
        REFERENCES `audience` (`username`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `platform` FOREIGN KEY (`platform_id`)
        REFERENCES `rating_platform` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `ticket` (
    `audience_username` VARCHAR(45) NOT NULL,
    `movie_session_id` INT NOT NULL,
    PRIMARY KEY (`audience_username` , `movie_session_id`),
    KEY `movie_session_idx` (`movie_session_id`),
    CONSTRAINT `audience_ticket` FOREIGN KEY (`audience_username`)
        REFERENCES `audience` (`username`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `movie_session` FOREIGN KEY (`movie_session_id`)
        REFERENCES `movie_session` (`id`)
        ON DELETE CASCADE ON UPDATE CASCADE
);