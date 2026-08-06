-- show every manga with its author
select
    manga.title,
    authors.author_name,
    manga.release_year,
    manga.publication_status
from manga
join authors
    on manga.author_id = authors.author_id
order by manga.title;


-- show manga currently being read
select
    manga.title,
    reading_progress.current_volume,
    reading_progress.volumes_owned,
    reading_progress.rating
from reading_progress
join manga
    on reading_progress.manga_id = manga.manga_id
where reading_progress.reading_status = 'Reading'
order by reading_progress.rating desc;


-- show completed manga
select
    manga.title,
    manga.total_volumes,
    reading_progress.rating
from manga
join reading_progress
    on manga.manga_id = reading_progress.manga_id
where reading_progress.reading_status = 'Completed'
order by reading_progress.rating desc;


-- show favourite manga
select
    manga.title,
    reading_progress.rating,
    reading_progress.notes
from reading_progress
join manga
    on reading_progress.manga_id = manga.manga_id
where reading_progress.favourite = 1
order by reading_progress.rating desc;


-- show manga rated 8.5 or higher
select
    manga.title,
    reading_progress.rating,
    reading_progress.reading_status
from manga
join reading_progress
    on manga.manga_id = reading_progress.manga_id
where reading_progress.rating >= 8.5
order by reading_progress.rating desc;