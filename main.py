from bottle import route, run, jinja2_template as template, redirect,abort,jinja2_view as view,url,request
import jinja2
from pymongo import MongoClient
from bson.objectid import ObjectId
from pagnation import Pagination
from math import ceil

PER_PAGE = 1


template.defaults = {
    'url': url,
    'site_name': 'CSV Display',
}

client = MongoClient()
db = client.test

def count_all_docs():
  return db["documents"].count()

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


@route('/docs/', defaults={'page': 1})
@route('/docs/list/<page:int>', name="list_page")
@view('templates/docs.html')
def show_docs(page):
  count = count_all_docs()
  docs = get_docs_for_page(page, PER_PAGE, count)
  if not docs or page < 1:
    abort(404)
  pagination = Pagination(page, PER_PAGE, count)
  return {
    "pagination":pagination,
    "docs":docs,
    "url_for_other_page":url_for_other_page,
    "sorted":sorted,
  }







run(host = 'localhost', port = 8080, debug = True)
