SELECT name FROM people
WHERE people.id IN
(SELECT DISTINCT person_id FROM stars
JOIN movies ON movies.id = movie_id
WHERE year = 2004)
ORDER BY birth ASC;