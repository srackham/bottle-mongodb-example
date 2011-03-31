# -*- coding: utf-8 -*-
import datetime
from mongoengine import Document, connect
from mongoengine import StringField, DateTimeField, FileField

DB_NAME = 'bottle_mongodb_example_mongoengine'

class Message(Document):
    nickname = StringField(required=True)
    text = StringField(required=True)
    date = DateTimeField(required=True, default=datetime.datetime.now)
    image_filename = StringField()
    image = FileField()
    thumb = FileField()

connect(DB_NAME)
