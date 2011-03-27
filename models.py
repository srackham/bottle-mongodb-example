# -*- coding: utf-8 -*-
import sys
import datetime
import mongokit
import gridfs

DB_NAME = 'bottle_mongodb_example'


class Message(mongokit.Document):
    __database__ = DB_NAME
    __collection__ = 'messages'
    structure = {
        'nickname': unicode,
        'text': unicode,
        'image': unicode,   # Image filename.
        'date': datetime.datetime,  # Creation timestamp.
    }
    required_fields=['nickname', 'text', 'date']
    default_values = {'date': datetime.datetime.now}
    use_dot_notation = True


# Create database connections AFTER model declarations.
con = mongokit.Connection()
con.register([Message])
db = con[DB_NAME]

# GridFS file systems.
imagesfs = gridfs.GridFS(db,'images')
thumbsfs = gridfs.GridFS(db,'thumbs')

# Export database and collections.
module = sys.modules[__name__]
module.db = db
module.messages = db.messages
module.imagesfs = imagesfs
module.thumbsfs = thumbsfs
