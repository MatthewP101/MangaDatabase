-- turn on foreign key checks in sqlite
pragma foreign_keys = on;


-- delete old tables when rebuilding the database
-- child tables must be deleted before parent tables
drop table if exists manga_genres;
drop table if exists reading_progress;
drop table if exists manga;
drop table if exists genres;
drop table if exists authors;


-- stores each manga author
create table authors (
    author_id integer primary key autoincrement,
    author_name text not null unique,
    country text default 'Japan'
);


-- stores the main information for each manga
create table manga (
    manga_id integer primary key autoincrement,
    title text not null unique,
    author_id integer not null,
    release_year integer,
    publication_status text not null,
    total_volumes integer,
    demographic text,
    synopsis text,

    -- connect each manga to an author
    foreign key (author_id)
        references authors(author_id),

    -- only allow expected publication statuses
    check (
        publication_status in (
            'Ongoing',
            'Completed',
            'Hiatus',
            'Cancelled'
        )
    ),

    -- stop negative volume values
    check (
        total_volumes is null
        or total_volumes >= 0
    )
);


-- stores the available manga genres
create table genres (
    genre_id integer primary key autoincrement,
    genre_name text not null unique
);


-- connects manga to genres
-- this allows one manga to have multiple genres
create table manga_genres (
    manga_id integer not null,
    genre_id integer not null,

    -- stop the same genre being added twice
    primary key (manga_id, genre_id),

    foreign key (manga_id)
        references manga(manga_id)
        on delete cascade,

    foreign key (genre_id)
        references genres(genre_id)
        on delete cascade
);


-- stores collection and reading information
create table reading_progress (
    progress_id integer primary key autoincrement,
    manga_id integer not null unique,
    volumes_owned integer not null default 0,
    current_volume integer not null default 0,
    reading_status text not null default 'Plan to Read',
    rating real,
    favourite integer not null default 0,
    notes text,

    foreign key (manga_id)
        references manga(manga_id)
        on delete cascade,

    -- stop negative progress values
    check (volumes_owned >= 0),
    check (current_volume >= 0),

    -- ratings can only be between 1 and 10
    check (
        rating is null
        or rating between 1 and 10
    ),

    -- sqlite uses 0 and 1 for false and true
    check (favourite in (0, 1)),

    -- only allow expected reading statuses
    check (
        reading_status in (
            'Plan to Read',
            'Reading',
            'Completed',
            'Paused',
            'Dropped'
        )
    )
);