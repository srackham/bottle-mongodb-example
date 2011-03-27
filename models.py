# -*- coding: utf-8 -*-
import sys
import datetime
import mongokit
from pymongo.objectid import ObjectId
import gridfs

DB_NAME = 'bottle_mongodb_example_mongokit'


class Message(mongokit.Document):
    __database__ = DB_NAME
    __collection__ = 'messages'
    structure = {
        'nickname': basestring,
        'text': basestring,
        'date': datetime.datetime,  # Creation timestamp.
        'image_id': ObjectId,
        'thumb_id': ObjectId,
        'image_filename': basestring,
    }
    required_fields = ['nickname', 'text', 'date']
    default_values = {'date': datetime.datetime.now}
    use_dot_notation = True

    def image(self):
        return fs.get(self.image_id)

    def thumb(self):
        return fs.get(self.thumb_id)

# Create database connections AFTER model declarations.
con = mongokit.Connection()
con.register([Message])
db = con[DB_NAME]

# GridFS file systems.
fs = gridfs.GridFS(db)

# Export database and collections.
module = sys.modules[__name__]
module.db = db
module.messages = db.messages
module.fs = fs
