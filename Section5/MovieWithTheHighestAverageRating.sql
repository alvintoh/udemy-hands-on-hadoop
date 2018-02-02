CREATE VIEW IF NOT EXISTS avgRatings AS
SELECT movieID, AVG(rating) as averageRating, COUNT(movieID) as ratingCount
FROM ratings
GROUP BY movieID
ORDER BY averageRating DESC;

SELECT n.title, averageRating, ratingCount 
FROM avgRatings t JOIN names n ON t.movieID = n.movieID
WHERE t.ratingCount > 10;