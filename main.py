from bottle import route, run, jinja2_template as template, redirect,abort,jinja2_view as view,url,request,static_file,response
#import jinja2
from pagnation import Pagination
import urllib
import os
import project_settings as settings
import csv_processor
import load_class


import time

current_milli_time = lambda: int(round(time.time() * 1000))


template.defaults = {
    'url': url,
    'site_name': settings.DEFAULT_SITE_NAME,
}

db_class = load_class.load_class(settings.DB_DRIVER_CLASS)
db = db_class()



def url_for_other_page(page):
  args = request.url_args.copy()
  args['page'] = page
  return url(request.route.name, **args)


@route('/docs/import')
@view('templates/import.html')
def import_csv():
  return {
          "current_collection": settings.DEFAULT_COLLECTION,
          "current_database": settings.DEFAULT_DB_NAME
  }


@route('/docs/import', method='POST')
@view('templates/import_finished.html')
def do_import_csv():
  upload = request.files.get('csv_file')
  if not upload:
    return {"message":"No File Found!"}
  file_path = settings.DEFAULT_TEMP_DIR+"/"+ str(current_milli_time)+upload.filename
  upload.save(file_path,overwrite=True)
  csv_rows = csv_processor.csv_to_json(file_path)
  return {
    "message":"Finished with "+str(len(csv_rows))+" rows uploaded",
    "number_of_rows":len(csv_rows)
    }


@route('/docs/export')
@view('templates/export.html')
def export_csv():
  file_name =  str(current_milli_time())+"_csv_file.csv"
  csv_processor.write_to_csv(settings.DEFAULT_TEMP_DIR+"/"+file_name)
  #static_file(file_name,root=settings.DEFAULT_TEMP_DIR,mimetype='text/csv')
  output = open(settings.DEFAULT_TEMP_DIR+"/"+file_name, 'r')
  response.headers['Content-Type'] = 'text/csv; charset=UTF-8'
  response.set_header('Cache-control', 'no-cache, must-revalidate')

  response.headers['Content-Disposition'] = 'attachment; filename='+file_name
  return output.read()


@route('/')
@view('templates/home.html')
def home():
  total_count = db.count_docs({})
  unscored_count = db.count_docs({"score":None})
  scored_count = db.count_docs({"score":{"$ne":None}})

  return {
    "total_count":total_count,
    "unscored_count":unscored_count,
    "scored_count":scored_count
  }


@route('/list')
@view('templates/list.html')
def list():
  docs = db.get_docs({})
  return dict(docs=docs)


@route('/docs/doc/<the_id>')
@view('templates/show.html')
def show(the_id):
  #print("id is: " +the_id)
  doc = db.get_document_by_id(the_id)

  return dict(doc=doc)


@route('/docs/list/<scored_status>/<page:int>', name="list_page")
@view('templates/docs.html')
def show_docs(scored_status="all",page=1):
  unscored = request.query.unscored
  print("scored_status is "+scored_status)
  query = {}
  if scored_status == "unscored" :
    query = {"score":None}
    count = db.count_docs(query)
  elif scored_status == "scored":
    query = {"score":{"$ne":None}}
    count = db.count_docs(query)
  elif scored_status == "all":
    #query = {"score":"9"}
    query = {}
    count = db.count_docs(query)
  else:
    abort(404,'Unknown Scored Status '+scored_status+' in request parameter.')

  docs = db.get_docs_for_page(page, settings.DEFAULT_RECORDS_PER_PAGE, count,query)
  if not docs or page < 1:
    abort(404, 'No '+scored_status+' records found.')
  pagination = Pagination(page, settings.DEFAULT_RECORDS_PER_PAGE, count)
  message = request.query.message
  return {
    "pagination":pagination,
    "docs":docs,
    "url_for_other_page":url_for_other_page,
    "count_all_scored_docs":db.count_scored_docs,
    "count_all_docs":db.count_docs,
    "sorted":sorted,
    "message":message,
    "scored_status":scored_status
  }

@route('/docs/list/<scored_status>/<page:int>', method='POST')
@view('templates/docs.html')
def do_show_docs(scored_status="all",page=1):
  the_ids = request.forms.getall('_id')
  print(the_ids)

  for the_id in the_ids:
    the_score = request.forms.get(the_id+'_score')
    print(the_id+'_score')
    message = ''
    if the_id and the_score and the_score.isdigit() :
      the_doc = db.get_document_by_id(the_id)
      the_doc["score"] = the_score
      the_doc = db.update_document_by_id(the_id,the_doc)
      message = "Score(s) saved!"
    elif not the_id:
      message = "Error : id not in request "
    elif not the_score:
      message = "Error : Score(s) not in request "
    elif not the_score.isdigit():
      message = "Error : Score(s) must be a number between 0 and 10 "

  message = urllib.parse.urlencode({"message":message})

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








run(host = '0.0.0.0', port = settings.DEFAULT_PORT, debug = True, reloader = True)
