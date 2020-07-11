SELECT name FROM people
WHERE people.id IN
( SELECT person_id FROM stars
JOIN movies ON movies.id = stars.movie_id
WHERE movie_id IN
( SELECT movie_id FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON people.id = stars.person_id
WHERE people.id IN
( SELECT people.id FROM people
WHERE name = "Kevin Bacon" AND birth = 1958)))
EXCEPT
SELECT name FROM people
WHERE name = "Kevin Bacon" AND birth = 1958;