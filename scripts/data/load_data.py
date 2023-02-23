from zipfile import ZipFile
from io import BytesIO
import urllib.request as urllib2
import pandas as pd
import os
from dotenv import load_dotenv
import glob

load_dotenv()

signature = os.getenv("DOWNLOAD_SIGNATURE")
url = "https://storage.googleapis.com/kaggle-data-sets/1069/1940/compressed/PS_20174392719_1491204439457_log.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20230223%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230223T091951Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature={signature}".format(
    signature=signature
)
file_name = "PS_20174392719_1491204439457_log.csv"
output_file = "resources/original_data/bank_fraud_raw_data.csv"
folder_split_files = "resources/split_data/"


r = urllib2.urlopen(url).read()
file = ZipFile(BytesIO(r))
file = file.open(file_name)
df = pd.read_csv(file)
df_fraud = df[df["isFraud"] == 1]
df_not_fraud_sampled = df[df["isFraud"] == 0].sample(n=100000)
df_sampled_shuffled = (
    pd.concat([df_fraud, df_not_fraud_sampled], ignore_index=True)
    .sample(frac=1)
    .reset_index(drop=True)
)
df_sampled_shuffled.to_csv(output_file, index=False)

files = glob.glob(folder_split_files + "*")
for f in files:
    os.remove(f)
