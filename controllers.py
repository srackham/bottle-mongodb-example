import datetime
import string
import random
import mimetypes
import cStringIO as StringIO

from bottle import request, response, get, post
from bottle import static_file, redirect, HTTPResponse
from bottle import mako_view as view

from PIL import Image
from pymongo.connection import Connection
from pymongo import DESCENDING
import gridfs

DEBUG = True

db = Connection().bottle_mongodb_example
imagesfs = gridfs.GridFS(db,'images')
thumbsfs = gridfs.GridFS(db,'thumbs')

def _unique_filename(filename):
    """ Return a unique filename based on filename to save in the database."""
    result = filename.rsplit('.', 1)
    result[0] = '%s-%s' % (result[0],
                  ''.join(random.sample(string.letters + string.digits, 10)))
    result = '.'.join(result)
    if imagesfs.exists({'result':result}):
        return _unique_filename(filename)
    else:
        return result

@get(['/', '/list', '/list/:page#\d+#'])
@view('list.mako')
def list(page=0):
    ''' List messages. '''
    PAGE_SIZE = 5
    page = int(page)
    prev_page = None
    if page > 0:
        prev_page = page - 1
    next_page = None
    if db.messages.count() > (page + 1) * PAGE_SIZE:
        next_page = page + 1
    messages = (db.messages.find()
                .sort('date', DESCENDING)
                .limit(PAGE_SIZE).skip(page * PAGE_SIZE))
    return {'messages': messages,
            'prev_page': prev_page,
            'next_page': next_page,
            }

@post('/create')
def create():
    ''' Save new message. '''
    if not (request.POST.get('nickname') and request.POST.get('text')):
        redirect('/')
    message = {'nickname': request.POST['nickname'],
               'text': request.POST['text'],
               'date': datetime.datetime.now()}
    if 'image' in request.files:
        upload = request.files['image']
        filename = _unique_filename(upload.filename)
        # Only accept appropriate file extensions
        if not filename.lower().endswith(
                ('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            redirect('/')
        message['image'] = filename
        # Save fullsize image
        imagesfs.put(upload.file, filename=filename)
        # Save thumbnail
        image = Image.open(imagesfs.get_version(filename))
        image.thumbnail((80, 60), Image.ANTIALIAS)
        data = StringIO.StringIO()
        image.save(data, image.format)
        data.seek(0)
        thumbsfs.put(data, filename=filename)
    db.messages.insert(message)
    redirect('/')

@get('/:collection#(images|thumbs)#/:filename')
def get_database_file(collection, filename):
    ''' Send image or image thumb from file stored in the database. '''
    import urllib
    filename = urllib.unquote_plus(filename)
    f = gridfs.GridFS(db, collection).get_version(filename)
    response.content_type = f.content_type or mimetypes.guess_type(filename)
    return HTTPResponse(f)

@get('/static/:filename#.+#')
def get_static_file(filename):
    ''' Send static files from ./static folder. '''
    return static_file(filename, root='./static')
