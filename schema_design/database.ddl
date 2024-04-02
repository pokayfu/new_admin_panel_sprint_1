CREATE SCHEMA content; 
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);
CREATE INDEX film_work_creation_date_idx ON content.film_work(creation_date); 
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone
);
CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);