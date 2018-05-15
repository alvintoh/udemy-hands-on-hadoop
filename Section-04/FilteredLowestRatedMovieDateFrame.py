from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

def loadMovieNames():
	movieNames = {}
	with open('ml-100k/u.item') as f:
		for line in f:
			fields = line.split('|')
			movieNames[int(fields[0])] = fields[1]
	return movieNames

def parseInput(line):
	fields = line.split()
	return Row(movieID = int(fields[1]), rating = float(fields[2]))

if __name__ == "__main__":
	# Create a SparkSession
	spark = SparkSession.builder.appName("PopularMovies").getOrCreate()

	# load up our movie ID -> name dictionary
	movieNames = loadMovieNames()

	# get the raw data
	lines = spark.sparkContext.textFile("hdfs:///user/maria_dev/ml-100k/u.data")

	# Convert it to a RDD of Row objects with (movieID, rating)
	movies = lines.map(parseInput)

	# Convert that to a DataFrame
	movieDataset = spark.createDataFrame(movies)

	# Compute counts of ratings for each movieID
	counts = movieDataset.groupBy("movieID").count()

	# Filter the count of ratings for movies < 10 or fewer times
	filteredCounts = counts.filter("count > 10")

	# Compute average rating for each movieID
	averageRatings = movieDataset.groupBy("movieID").avg("rating")

	# Join the two together (We now have movieID, avg(rating), and count columns)
	averagesAndCounts = filteredCounts.join(averageRatings, "movieID")

	# Pull the top 10 results
	topTen = averagesAndCounts.orderBy("avg(rating)").take(10)

    # Print them out, converting movie ID's to names as we go.
    for movie in topTen:
   		print (movieNames[movie[0]], movie[1], movie[2])

    # Stop the session

