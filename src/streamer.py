from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql.functions import expr
from pyspark.sql.window import Window
import time
from pathlib import Path

spark = SparkSession.builder \
    .appName("GitHubCommitProcessing") \
    .getOrCreate()

input_directory = "input_files"
output_directory = "output_files"
checkpoint_directory = "checkpoints"

Path(input_directory).mkdir(parents=True, exist_ok=True)
Path(output_directory).mkdir(parents=True, exist_ok=True)
Path(checkpoint_directory).mkdir(parents=True, exist_ok=True)

watermark_col = "date"
watermark_duration = "4 weeks"

q1 = spark.readStream \
    .json(input_directory, "repo STRING, author STRING, date TIMESTAMP", multiLine=True) \
    .withWatermark(watermark_col, watermark_duration) \
    .groupBy(["author", "repo", expr("window(" + watermark_col + ", '" + watermark_duration + "')")]) \
    .count() \
    .writeStream \
    .outputMode("append") \
    .trigger(processingTime='5 seconds') \
    .format("json") \
    .option("path", output_directory) \
    .option("checkpointLocation", checkpoint_directory) \
    .start()

time.sleep(30)

q1.stop()