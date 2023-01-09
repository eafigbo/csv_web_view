import sqlite3
import json
import project_settings as settings
from bson.objectid import ObjectId
from math import ceil
import uuid


class SQLiteDriver():
  connection = None
  cursor = None
  
  def __init__(self):
    self.connection = sqlite3.connect(settings.DEFAULT_DB_NAME)
    self.cursor = self.connection.cursor()
    #create table if it does not already exist
    self.cursor.execute(settings.SQLITE_CREATE_TABLE_STATEMENT)



  def count_docs(self,query={}):
    if(len(query) == 0):
        return self.cursor.execute('''select count(json_field) from data''').fetchone()[0]
    elif(query.get("score",None) is None):
        return self.cursor.execute('''select count(json_field) from data where json_extract(json_field,'$.score') is NULL''').fetchone()[0]
    else:
        return self.cursor.execute('''select count(json_field) from data where json_extract(json_field,'$.score') is not NULL''').fetchone()[0]


  def get_docs(self,query={}):
    if(len(query) == 0):
        return dict_list(self.cursor.execute('''select json_field from data''').fetchall())
    elif(query.get("score",None) is None):
        return dict_list(self.cursor.execute('''select json_field from data where json_extract(json_field,'$.score') is NULL''').fetchall())
    else:
        return dict_list(self.cursor.execute('''select json_field from data where json_extract(json_field,'$.score') is not NULL''').fetchall())


  def count_scored_docs(self):
    return self.cursor.execute('''select count(json_field) from data where json_extract(json_field,'$.score') is not NULL''').fetchone()[0]

  def get_document_by_id(self,the_id):
    return json.loads(self.cursor.execute('''select json_field from data where json_extract(json_field,'$._id') = ?''',[the_id]).fetchone()[0])

  def update_document_by_id(self,the_id,the_doc):

    self.cursor.execute('''update data set json_field = ? where json_extract(json_field,'$._id') = ?''',[json.dumps(the_doc),the_id])
    self.connection.commit()

    return json.loads(self.cursor.execute('''select json_field from data where json_extract(json_field,'$._id') = ?''',[the_id]).fetchone()[0])

  def create(self,the_doc):
    #set unique id
    the_doc['_id'] = str(uuid.uuid4())
    self.cursor.execute('''insert into data(json_field) values(?)''',[json.dumps(the_doc)])
    self.connection.commit()

    return json.loads(self.cursor.execute('''select json_field from data where json_extract(json_field,'$._id') = ?''',[the_doc['_id']]).fetchone()[0])['_id']


  def get_docs_for_page(self,page, PER_PAGE, count,query = {}):
    print('count arg is '+str(count))
    print("count is "+ str(ceil(count/float(PER_PAGE))))
    if (page <1 or page > ceil(count/float(PER_PAGE))):
      return None
    result = self.get_docs(query)#.sort('_id')[((PER_PAGE * page) - PER_PAGE):((PER_PAGE * page))]
    newresult_list = sorted(result, key=lambda d: d['_id']) 
    return newresult_list[((PER_PAGE * page) - PER_PAGE):((PER_PAGE * page))]


def dict_list(json_list):
  dict_list = []
  for item in json_list:
    dict_list.append(json.loads(item[0]))
  return dict_list
