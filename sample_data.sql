-- turn on foreign key checks
pragma foreign_keys = on;


-- add manga authors
insert into authors (author_name, country)
values
    ('Kentaro Miura', 'Japan'),
    ('Tatsuki Fujimoto', 'Japan'),
    ('Naoki Urasawa', 'Japan'),
    ('Tsugumi Ohba', 'Japan'),
    ('Hiromu Arakawa', 'Japan'),
    ('Sui Ishida', 'Japan'),
    ('Inio Asano', 'Japan'),
    ('Hajime Isayama', 'Japan');


-- add manga series
-- author ids are found using the authors table
insert into manga (
    title,
    author_id,
    release_year,
    publication_status,
    total_volumes,
    demographic,
    synopsis
)
values
    (
        'Berserk',
        (
            select author_id
            from authors
            where author_name = 'Kentaro Miura'
        ),
        1989,
        'Ongoing',
        null,
        'Seinen',
        'A dark fantasy story following Guts and his struggle against fate.'
    ),

    (
        'Chainsaw Man',
        (
            select author_id
            from authors
            where author_name = 'Tatsuki Fujimoto'
        ),
        2018,
        'Ongoing',
        null,
        'Shonen',
        'A young devil hunter gains the power of the Chainsaw Devil.'
    ),

    (
        'Monster',
        (
            select author_id
            from authors
            where author_name = 'Naoki Urasawa'
        ),
        1994,
        'Completed',
        18,
        'Seinen',
        'A surgeon searches for a dangerous former patient whose life he saved.'
    ),

    (
        'Death Note',
        (
            select author_id
            from authors
            where author_name = 'Tsugumi Ohba'
        ),
        2003,
        'Completed',
        12,
        'Shonen',
        'A student discovers a notebook capable of killing anyone whose name is written inside.'
    ),

    (
        'Fullmetal Alchemist',
        (
            select author_id
            from authors
            where author_name = 'Hiromu Arakawa'
        ),
        2001,
        'Completed',
        27,
        'Shonen',
        'Two brothers search for the Philosopher Stone after a failed alchemy experiment.'
    ),

    (
        'Tokyo Ghoul',
        (
            select author_id
            from authors
            where author_name = 'Sui Ishida'
        ),
        2011,
        'Completed',
        14,
        'Seinen',
        'A university student becomes trapped between the human and ghoul worlds.'
    ),

    (
        'Goodnight Punpun',
        (
            select author_id
            from authors
            where author_name = 'Inio Asano'
        ),
        2007,
        'Completed',
        13,
        'Seinen',
        'A psychological coming-of-age story following Punpun through childhood and adulthood.'
    ),

    (
        'Attack on Titan',
        (
            select author_id
            from authors
            where author_name = 'Hajime Isayama'
        ),
        2009,
        'Completed',
        34,
        'Shonen',
        'Humanity fights for survival against giant humanoid creatures known as Titans.'
    );


-- add available genres
insert into genres (genre_name)
values
    ('Action'),
    ('Adventure'),
    ('Dark Fantasy'),
    ('Drama'),
    ('Fantasy'),
    ('Horror'),
    ('Mystery'),
    ('Psychological'),
    ('Science Fiction'),
    ('Supernatural'),
    ('Thriller');

    -- connect manga to their genres
-- the select statements find the correct ids by name

insert into manga_genres (manga_id, genre_id)
values
    (
        (
            select manga_id
            from manga
            where title = 'Berserk'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Dark Fantasy'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Berserk'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Action'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Chainsaw Man'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Action'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Chainsaw Man'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Supernatural'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Monster'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Psychological'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Monster'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Thriller'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Death Note'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Mystery'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Death Note'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Supernatural'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Fullmetal Alchemist'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Adventure'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Fullmetal Alchemist'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Fantasy'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Tokyo Ghoul'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Horror'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Tokyo Ghoul'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Dark Fantasy'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Goodnight Punpun'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Drama'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Goodnight Punpun'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Psychological'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Attack on Titan'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Action'
        )
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Attack on Titan'
        ),
        (
            select genre_id
            from genres
            where genre_name = 'Dark Fantasy'
        )
    );

    -- add reading and collection progress for each manga
insert into reading_progress (
    manga_id,
    volumes_owned,
    current_volume,
    reading_status,
    rating,
    favourite,
    notes
)
values
    (
        (
            select manga_id
            from manga
            where title = 'Berserk'
        ),
        8,
        8,
        'Reading',
        9.5,
        1,
        'great artwork and dark fantasy story'
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Chainsaw Man'
        ),
        6,
        6,
        'Reading',
        8.5,
        1,
        'fast paced and unpredictable'
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Monster'
        ),
        18,
        18,
        'Completed',
        9.0,
        1,
        'strong psychological thriller'
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Death Note'
        ),
        12,
        12,
        'Completed',
        8.5,
        0,
        'good mystery and strategy'
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Fullmetal Alchemist'
        ),
        10,
        7,
        'Reading',
        8.0,
        0,
        'good world building and characters'
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Tokyo Ghoul'
        ),
        14,
        14,
        'Completed',
        8.0,
        0,
        'interesting horror and identity themes'
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Goodnight Punpun'
        ),
        4,
        3,
        'Paused',
        8.5,
        0,
        'heavy story that i am taking slowly'
    ),

    (
        (
            select manga_id
            from manga
            where title = 'Attack on Titan'
        ),
        34,
        34,
        'Completed',
        9.0,
        1,
        'strong story with good long term setup'
    );