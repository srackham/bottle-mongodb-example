# -*- coding: utf-8 -*-
import mimetypes
import cStringIO as StringIO

from bottle import request, response, get, post
from bottle import static_file, redirect, HTTPResponse
from bottle import mako_view as view
from PIL import Image
from pymongo import DESCENDING
from pymongo.objectid import ObjectId
import models as db


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
    msgs = (db.messages.Message.find()
                .sort('date', DESCENDING)
                .limit(PAGE_SIZE).skip(page * PAGE_SIZE))
    return {'messages': msgs,
            'prev_page': prev_page,
            'next_page': next_page,
           }

@post('/create')
def create():
    ''' Save new message. '''
    if not (request.POST.get('nickname') and request.POST.get('text')):
        redirect('/')
    msg = db.messages.Message()
    msg.nickname = request.POST.get('nickname')
    msg.text = request.POST.get('text')
    msg.save()
    if 'image' in request.files:
        upload = request.files['image']
        # Only accept appropriate file extensions
        if not upload.filename.lower().endswith(
                ('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            redirect('/')
        mime = mimetypes.guess_type(upload.filename)[0]
        # Save fullsize image
        file_id = msg.fs.put(upload.file, filename='image', content_type=mime)
        # Save thumbnail
        image = Image.open(db.fs.get(file_id))
        image.thumbnail((80, 60), Image.ANTIALIAS)
        data = StringIO.StringIO()
        image.save(data, image.format)
        data.seek(0)
        msg.fs.put(data, filename='thumb', content_type=mime)
        # Update image filename after images have successfully uploaded.
        msg.save()
    redirect('/')

@get('/image/:file_id')
def get_image(file_id):
    ''' Send image or image thumb from file stored in the database. '''
    f = db.fs.get(ObjectId(file_id))
    response.content_type = f.content_type
    return HTTPResponse(f)

@get('/static/:filename#.+#')
def get_static_file(filename):
    ''' Send static files from ./static folder. '''
    return static_file(filename, root='./static')
