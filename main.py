from bottle import route, run, jinja2_template as template, redirect,abort,jinja2_view as view,url,request,static_file
import jinja2
from pymongo import MongoClient
from bson.objectid import ObjectId
from pagnation import Pagination
from math import ceil
import urllib
import os
import project_settings as settings



template.defaults = {
    'url': url,
    'site_name': settings.DEFAULT_SITE_NAME,
}

client = MongoClient(settings.DEFAULT_DB_HOST, settings.DEFAULT_DB_PORT)
db = client[settings.DEFAULT_DB_NAME]

def count_all_docs(query={}):
  return db[settings.DEFAULT_COLLECTION].find(query).count()

def count_all_scored_docs():
  return db[settings.DEFAULT_COLLECTION].find({'score':{ '$exists': True, '$ne':''}}).count()

def get_docs_for_page(page, PER_PAGE, count,query = {}):
  print "count is "+ str(ceil(count/float(PER_PAGE)))
  if (page <1 or page > ceil(count/float(PER_PAGE))):
    return None
  result = db[settings.DEFAULT_COLLECTION].find(query).sort('_id')[((PER_PAGE * page) - PER_PAGE):((PER_PAGE * page))]
  return result


def url_for_other_page(page):
  args = request.url_args.copy()
  args['page'] = page
  return url(request.route.name, **args)


@route('/list')
@view('templates/list.html')
def list():
  docs = db[settings.DEFAULT_COLLECTION].find()
  return dict(docs=docs)


@route('/docs/doc/<the_id>')
@view('templates/show.html')
def show(the_id):
  print "id is: " +the_id
  doc = db[settings.DEFAULT_COLLECTION].find_one({"_id":ObjectId(the_id)})

  return dict(doc=doc)


@route('/docs/list/<scored_status>/<page:int>', name="list_page")
@view('templates/docs.html')
def show_docs(scored_status="all",page=1):
  unscored = request.query.unscored
  print "scored_status is "+scored_status
  query = {}
  if scored_status == "unscored" :
    query = {"score":None}
    count = count_all_docs(query)
  elif scored_status == "all":
    #query = {"score":"9"}
    query = {}
  else:
    abort(404)
  count = count_all_docs(query)

  docs = get_docs_for_page(page, settings.DEFAULT_RECORDS_PER_PAGE, count,query)
  if not docs or page < 1:
    abort(404)
  pagination = Pagination(page, settings.DEFAULT_RECORDS_PER_PAGE, count)
  message = request.query.message
  return {
    "pagination":pagination,
    "docs":docs,
    "url_for_other_page":url_for_other_page,
    "count_all_scored_docs":count_all_scored_docs,
    "count_all_docs":count_all_docs,
    "sorted":sorted,
    "message":message,
    "scored_status":scored_status
  }

@route('/docs/list/<scored_status>/<page:int>', method='POST')
@view('templates/docs.html')
def show_docs(scored_status="all",page=1):
  the_id = request.forms.get('_id')
  the_score = request.forms.get('score')
  message = ''
  if the_id and the_score and the_score.isdigit() :
    the_doc = db[settings.DEFAULT_COLLECTION].find_one({"_id":ObjectId(the_id)})
    the_doc["score"] = the_score
    the_doc = db[settings.DEFAULT_COLLECTION].save(the_doc)
    message = "Score saved!"
  elif not the_id:
    message = "Error : id not in request "
  elif not the_score:
    message = "Error : Score not in request "
  elif not the_score.isdigit():
    message = "Error : Score must be a number between 0 and 10 "

  message = urllib.urlencode({"message":message})

  redirect("/docs/list/"+scored_status+"/"+str(page)+"?"+message)


@route('/static/img/<filename:re:[^\s]+(\.(?i)(jpg|png|gif|bmp))$>')
def send_image(filename):
  the_filename, file_extension = os.path.splitext('filename')
  return static_file(filename, root='static/img', mimetype='image/'+file_extension.replace('.',''))

@route('/static/js/<filename:path>')
def send_js(filename):
  return static_file(filename, root='static/js')

@route('/static/<filename:path>')
def send_html(filename):
  return static_file(filename, root='static')








run(host = '0.0.0.0', port = 8080, debug = True)
