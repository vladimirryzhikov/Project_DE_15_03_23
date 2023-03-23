from pyspark import SparkContext

# create a SparkContext object
sc = SparkContext("local", "WordCount")

# load the text file into an RDD
lines = sc.textFile("/home/vladimir/Documents/DE_project/status_localstack.txt")

# split each line into words
words = lines.flatMap(lambda line: line.split())

# count the number of occurrences of each word
word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y)

# print the results
for word, count in word_counts.collect():
    print("{}: {}".format(word, count))
