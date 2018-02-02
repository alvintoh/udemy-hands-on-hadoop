CREATE VIEW IF NOT EXISTS avgRatings AS
SELECT movieID, avg(rating) as averageRating, count(movieID) as ratingCount
FROM ratings
WHERE ratingCount > 10
GROUP BY movieID
ORDER BY averageRating DESC;

SELECT n.title, t.averageRating, t.ratingCount 
FROM avgRatings t JOIN names n ON t.movieID = n.movieID;