# -*- coding: utf-8 -*-
import sys
import datetime
import mongokit
import gridfs

DB_NAME = 'bottle_mongodb_example_mongokit'


class Message(mongokit.Document):
    __database__ = DB_NAME
    __collection__ = 'messages'
    structure = {
        'nickname': basestring,
        'text': basestring,
        'date': datetime.datetime,  # Creation timestamp.
    }
    gridfs = {'files':['image', 'thumb']}
    required_fields = ['nickname', 'text', 'date']
    default_values = {'date': datetime.datetime.now}
    use_dot_notation = True

    def has_image(self):
      try:
        self.fs.get_version('image')
        return True
      except:
        return False

    def image_id(self):
        return self.fs.get_version('image')._id

    def thumb_id(self):
        return self.fs.get_version('thumb')._id

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
