_# Databricks notebook source

# DBTITLE 1,Image Processing with Databricks
# MAGIC %md
# MAGIC # Cookbook: Image Processing
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to process a large number of images stored in cloud storage. This could be for tasks like resizing, watermarking, or feature extraction for machine learning.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This recipe demonstrates how to use Spark's **binary file data source** and **Pandas UDFs** to process images in a distributed manner.
# MAGIC 
# MAGIC - **Binary File Data Source**: Reads images into a DataFrame with columns for path, modification time, length, and content.
# MAGIC - **Pandas UDFs**: Allows you to apply Python libraries like Pillow to the image data in a distributed fashion.

# COMMAND ----------

# DBTITLE 1,Read Images into a DataFrame
# In a real-world scenario, you would point this to your own image directory
image_dir = "/databricks-datasets/cctv_videos/train_images/"

# Use the binary file data source to read the images
# The `recursiveFileLookup` option is useful for nested directories
images_df = spark.read.format("binaryFile") \
  .option("pathGlobFilter", "*.jpg") \
  .option("recursiveFileLookup", "true") \
  .load(image_dir)

display(images_df)

# COMMAND ----------

# DBTITLE 1,Define an Image Processing UDF
from PIL import Image
import io

def resize_image(content):
  img = Image.open(io.BytesIO(content))
  resized_img = img.resize((100, 100))
  
  # Convert the resized image back to bytes
  byte_arr = io.BytesIO()
  resized_img.save(byte_arr, format='JPEG')
  return byte_arr.getvalue()

# COMMAND ----------

# DBTITLE 1,Apply the UDF to the DataFrame
from pyspark.sql.functions import udf
from pyspark.sql.types import BinaryType

# Register the UDF
resize_image_udf = udf(resize_image, BinaryType())

# Apply the UDF to the content column
resized_images_df = images_df.withColumn("resized_content", resize_image_udf("content"))

display(resized_images_df)

# COMMAND ----------

# DBTITLE 1,Best Practices
# MAGIC %md
# MAGIC ### Use Binary File Data Source
# MAGIC 
# MAGIC The binary file data source is the most efficient way to read a large number of small files (like images) in Spark.
# MAGIC 
# MAGIC ### Use Pandas UDFs for Complex Processing
# MAGIC 
# MAGIC For more complex image processing tasks, consider using Pandas UDFs. They can provide better performance than regular UDFs by leveraging Apache Arrow and vectorization.
# MAGIC 
# MAGIC ### Handle Large Images
# MAGIC 
# MAGIC If you are working with very large images, you may need to adjust your Spark configuration (e.g., increase driver and executor memory) to avoid out-of-memory errors.
# MAGIC 
# MAGIC ### Attribution
# MAGIC 
# MAGIC This recipe is based on best practices from the Databricks documentation and the Spark community.
