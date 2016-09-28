import csv
import argparse
import pprint
from pymongo import MongoClient
import  codecs
import cStringIO
from unicode_csv import UnicodeReader,UnicodeWriter,UTF8Recoder
from bson.json_util import dumps
import json
import project_settings as settings


client = MongoClient(settings.DEFAULT_DB_HOST, settings.DEFAULT_DB_PORT)
db = client[settings.DEFAULT_DB_NAME]

pp = pprint.PrettyPrinter(indent = 2)



parser = argparse.ArgumentParser(description='Module that reads a csv '+\
'file and pumps it into a MongoDB database')
parser.add_argument("--mode",  help="read (read from csv file to database) or write (write from database to csv file)")
parser.add_argument("file_path")
args = parser.parse_args()

def csv_to_json(csv_file):
  csv_rows = []
  with open(csv_file, 'rU') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter = ',' , quotechar = '"', dialect=csv.excel_tab)
    title = csv_reader.fieldnames
    count = 0
    for row in csv_reader:
      csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
      count = count + 1
      print "row"+ `count`
    #pp.pprint(csv_rows)

    save_to_db(csv_rows)
    return csv_rows


def save_to_db(json_array):
  for doc in json_array:
    doc_id = db[settings.DEFAULT_COLLECTION].insert_one(doc).inserted_id
    print doc_id

def get_docs(query = {}):
  result = db[settings.DEFAULT_COLLECTION].find(query)
  return result


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
  # csv.py doesn't do Unicode; encode temporarily as UTF-8:
  csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
  for row in csv_reader:
    # decode UTF-8 back to Unicode, cell by cell:
    yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
  for line in unicode_csv_data:
    yield line.encode('utf-8')


def write_to_csv(file_name):
  documents = get_docs()
  serialized_documents = json.loads(dumps(documents))
  csv_file = open(file_name,'w')
  csv_writer = UnicodeWriter(csv_file, dialect='excel')
  count = 0
  for doc in serialized_documents:
    doc.pop('_id',None)
    if count == 0:
      header = doc.keys()
      header.sort()
      csv_writer.writerow(header)
      count = count+1
    csv_writer.writerow(doc.values())

  csv_file.close()




if args.file_path:
  if args.mode == "r":
    csv_to_json(args.file_path)
  elif args.mode == "w":
    write_to_csv(args.file_path)
