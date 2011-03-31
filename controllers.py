# -*- coding: utf-8 -*-
import mimetypes
import cStringIO as StringIO

from bottle import request, response, get, post
from bottle import static_file, redirect, HTTPResponse
from bottle import mako_view as view
from PIL import Image
from pymongo.objectid import ObjectId
from models import Message

PAGE_SIZE = 5

@get(['/', '/list', '/list/:page#\d+#'])
@view('list.mako')
def list(page=0):
    ''' List messages. '''
    page = int(page)
    prev_page = None
    next_page = None
    if page > 0:
        prev_page = page - 1
    if Message.objects.count() > (page + 1) * PAGE_SIZE:
        next_page = page + 1
    msgs = (Message.objects
            .order_by('-date')
            .skip(page * PAGE_SIZE)
            .limit(PAGE_SIZE))
    return {'messages': msgs,
            'prev_page': prev_page,
            'next_page': next_page,
           }

@post('/create')
def create():
    ''' Save new message. '''
    if not (request.POST.get('nickname') and request.POST.get('text')):
        redirect('/')
    msg = Message()
    msg.nickname = request.POST['nickname']
    msg.text = request.POST['text']
    if 'image' in request.files:
        upload = request.files['image']
        if not upload.filename.lower().endswith(
                ('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            redirect('/')
        mime = mimetypes.guess_type(upload.filename)[0]
        msg.image_filename = upload.filename
        # Save fullsize image
        msg.image.put(upload.file, content_type=mime)
        # Create and save thumbnail
        image = Image.open(msg.image)
        image.thumbnail((80, 60), Image.ANTIALIAS)
        data = StringIO.StringIO()
        image.save(data, image.format)
        data.seek(0)
        msg.thumb.put(data, content_type=mime)
    msg.save()
    redirect('/')

@get('/:image_type#(image|thumb)#/:docid')
def get_image(image_type, docid):
    ''' Send image or thumbnail from file stored in the database. '''
    f = Message.objects.with_id(ObjectId(docid))[image_type]
    response.content_type = f.content_type
    return HTTPResponse(f)

@get('/static/:filename#.+#')
def get_static_file(filename):
    ''' Send static files from ./static folder. '''
    return static_file(filename, root='./static')
