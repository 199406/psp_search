import json
import pandas as pd


def csv_to_json(csv_file):
    return csv_file.to_dict(orient='records')


path = "./psp_7000.csv"
csv_file = pd.read_csv(path)
data = csv_to_json(csv_file)

json_file_path = "./psp_7000.json"

# Write JSON data to file
with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file)
