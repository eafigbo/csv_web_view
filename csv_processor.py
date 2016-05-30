import csv
import argparse
import pprint
from pymongo import MongoClient

client = MongoClient()

db = client.test

pp = pprint.PrettyPrinter(indent = 2)



parser = argparse.ArgumentParser(description='Module that reads a csv '+\
'file and pumps it into a MongoDB database')
parser.add_argument("file_path")
args = parser.parse_args()

def csv_to_json(csv_file):
  csv_rows = []
  with open(csv_file, 'rb') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter = ',' , quotechar = '"')
    title = csv_reader.fieldnames
    for row in csv_reader:
      csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
    pp.pprint(csv_rows)

    save_to_db(csv_rows)
    return csv_rows


def save_to_db(json_array):
  for doc in json_array:
    doc_id = db['documents'].insert_one(doc).inserted_id
    print doc_id



if args.file_path:
  csv_to_json(args.file_path)
