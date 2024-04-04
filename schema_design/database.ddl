CREATE SCHEMA content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT  CHECK (rating >= 0 AND rating <= 100),
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT,
    created timestamp with time zone,
    modified timestamp with time zone,
    description TEXT,
    CONSTRAINT genre_pkey PRIMARY KEY (id)
);

CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date); 

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role text NOT NULL,
    created timestamp with time zone,
    CONSTRAINT person_film_work_pkey PRIMARY KEY (id),
    CONSTRAINT "Filmwork" FOREIGN KEY (film_work_id)
        REFERENCES content.film_work (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "Person" FOREIGN KEY (person_id)
        REFERENCES content.person (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);

CREATE UNIQUE INDEX film_work_person_id_role ON content.person_film_work (film_work_id, person_id, role);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created timestamp with time zone,
    id uuid PRIMARY KEY,
    CONSTRAINT genre_film_work_pkey PRIMARY KEY (film_work_id, genre_id),
    CONSTRAINT genre_film_work_film_work_id_genre_id_uniq UNIQUE (film_work_id, genre_id),
    CONSTRAINT "Filmwork" FOREIGN KEY (film_work_id)
        REFERENCES content.film_work (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "Genre" FOREIGN KEY (genre_id)
        REFERENCES content.genre (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);