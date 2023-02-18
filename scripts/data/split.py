import pandas as pd

folder_path = "resources/original_data/"
data = pd.read_csv(folder_path + "bank_fraud_raw_data.csv")
nb_rows = len(data)
nb_chunks = 10
chunk_size = int(nb_rows / nb_chunks)

for i in range(nb_chunks):
    data_ = data.iloc[i * chunk_size : (i + 1) * chunk_size]
    data_.to_csv(folder_path + f"bank_fraud_raw_data_{i}.csv", index=False)
