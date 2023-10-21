from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
from pathlib import Path
from os.path import join

spark = SparkSession.builder \
    .appName("GitHubCommitProcessing") \
    .getOrCreate()

input_directory = "input_files/*"
output_directory = "output_files"
checkpoint_directory = "checkpoints"

Path(input_directory).mkdir(parents=True, exist_ok=True)
Path(output_directory).mkdir(parents=True, exist_ok=True)
Path(checkpoint_directory).mkdir(parents=True, exist_ok=True)

watermark_col = "date"
watermark_duration = "4 weeks"

q = spark.readStream \
    .json(input_directory, "repo STRING, author STRING, date TIMESTAMP", multiLine=True) \
    .withWatermark(watermark_col, watermark_duration) \
    .groupBy(["author", "repo", expr("window(" + watermark_col + ", '" + watermark_duration + "')")]) \
    .count() \
    .writeStream \
    .outputMode("append") \
    .trigger(processingTime='1 seconds') \
    .format("json") \
    .option("path", output_directory) \
    .option("checkpointLocation", checkpoint_directory) \
    .start()

q.awaitTermination()