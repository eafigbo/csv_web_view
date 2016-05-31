from bottle import route, run, jinja2_template as template, redirect,abort,jinja2_view as view,url,request,static_file
import jinja2
from pymongo import MongoClient
from bson.objectid import ObjectId
from pagnation import Pagination
from math import ceil
import urllib
import os

PER_PAGE = 1


template.defaults = {
    'url': url,
    'site_name': 'CSV Display',
}

client = MongoClient()
db = client.test

def count_all_docs():
  return db["documents"].count()

def count_all_scored_docs():
  return db["documents"].find({'score':{ '$exists': True, '$ne':''}}).count()

def get_docs_for_page(page, PER_PAGE, count):
  print "count is "+ str(ceil(count/float(PER_PAGE)))
  if (page <1 or page > ceil(count/float(PER_PAGE))):
    return None
  return db["documents"].find().sort('_id')[((PER_PAGE * page) - PER_PAGE):((PER_PAGE * page))]


def url_for_other_page(page):
  args = request.url_args.copy()
  args['page'] = page
  return url(request.route.name, **args)


@route('/list')
@view('templates/list.html')
def list():
  docs = db["documents"].find()
  return dict(docs=docs)


@route('/docs/doc/<the_id>')
@view('templates/show.html')
def show(the_id):
  print "id is: " +the_id
  doc = db["documents"].find_one({"_id":ObjectId(the_id)})

  return dict(doc=doc)


@route('/docs/list/<page:int>', name="list_page")
@view('templates/docs.html')
def show_docs(page=1):
  count = count_all_docs()
  docs = get_docs_for_page(page, PER_PAGE, count)
  if not docs or page < 1:
    abort(404)
  pagination = Pagination(page, PER_PAGE, count)
  message = request.query.message
  return {
    "pagination":pagination,
    "docs":docs,
    "url_for_other_page":url_for_other_page,
    "count_all_scored_docs":count_all_scored_docs,
    "count_all_docs":count_all_docs,
    "sorted":sorted,
    "message":message
  }

@route('/docs/list/<page:int>', method='POST')
@view('templates/docs.html')
def show_docs(page=1):
  the_id = request.forms.get('_id')
  the_score = request.forms.get('score')
  message = ''
  if the_id and the_score and the_score.isdigit() :
    the_doc = db["documents"].find_one({"_id":ObjectId(the_id)})
    the_doc["score"] = the_score
    the_doc = db["documents"].save(the_doc)
    message = "Score saved!"
  elif not the_id:
    message = "Error : id not in request "
  elif not the_score:
    message = "Error : Score not in request "
  elif not the_score.isdigit():
    message = "Error : Score must be a number between 0 and 10 "

  message = urllib.urlencode({"message":message})

  redirect("/docs/list/"+str(page)+"?"+message)


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










run(host = 'localhost', port = 8080, debug = True)
