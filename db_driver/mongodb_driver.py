from pymongo import MongoClient
import project_settings as settings
from bson.objectid import ObjectId
from math import ceil



class MongoDriver():
  client = None
  db = None
  
  def __init__(self):
    self.client = MongoClient(settings.DEFAULT_DB_HOST, settings.DEFAULT_DB_PORT)
    self.db = self.client[settings.DEFAULT_DB_NAME]

  def count_docs(self,query={}):
    return self.db[settings.DEFAULT_COLLECTION].count_documents(query)

  def get_docs(self,query={}):
    return self.db[settings.DEFAULT_COLLECTION].find(query)

  def count_scored_docs(self):
    return self.db[settings.DEFAULT_COLLECTION].count_documents({'score':{ '$exists': True, '$ne':''}})

  def get_document_by_id(self,the_id):
    return self.db[settings.DEFAULT_COLLECTION].find_one({"_id":ObjectId(the_id)})

  def update_document_by_id(self,the_id,the_doc):
    the_doc = self.db[settings.DEFAULT_COLLECTION].replace_one({"_id":ObjectId(the_id)},the_doc)
    return the_doc

  def create(self,doc):
    return self.db[settings.DEFAULT_COLLECTION].insert_one(doc)


  def get_docs_for_page(self,page, PER_PAGE, count,query = {}):
    print("count is "+ str(ceil(count/float(PER_PAGE))))
    if (page <1 or page > ceil(count/float(PER_PAGE))):
      return None
    result = self.db[settings.DEFAULT_COLLECTION].find(query).sort('_id')[((PER_PAGE * page) - PER_PAGE):((PER_PAGE * page))]
    return result
