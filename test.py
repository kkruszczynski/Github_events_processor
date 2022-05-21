#
# # Import SparkSession
# from pyspark.sql import SparkSession
# import os
# # Create SparkSession
# spark = SparkSession.builder \
#       .master("local[1]") \
#       .appName("SparkByExamples.com") \
#       .getOrCreate()
# import gzip
# import shutil
# with gzip.open('file.txt.gz', 'rb') as f_in:
#     with open('file.txt', 'wb') as f_out:
#         shutil.copyfileobj(f_in, f_out)

import json
import os
import pandas as pd

def read_json_data(path):
    with open(path) as json_file:
        data = json.load(json_file)
    json_file.close()
    return data

path_to_data=f"{os.getcwd()}\\.data\\2022-01-01-15.json"
path_to_data=f"{os.getcwd()}\\.data\\2022-01-01-0.json.gz"

# if __name__=="__main__":
#     input_file=read_json_data(path_to_data)
df = pd.read_json(path_to_data, lines=True, compression='gzip')
df.tail()
