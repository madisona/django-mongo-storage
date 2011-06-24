
from django.conf import settings
from django.core.files.storage import Storage

from bson.errors import InvalidId
from bson.objectid import ObjectId
from gridfs import GridFS
from pymongo import Connection

__all__ = ('GridFSStorage',)

class GridFSStorage(Storage):
    """
    A storage adapter to use MongoDB's GridFS file storage

    Because this module checks the settings to see what the
    right connection settings should be, you can't instantiate
    this module in your settings.py. Instead, if you want specific
    settings in a particular model that differ from the default,
    instantiate the storage object in that model.

    settings.py would look something like this:
    GRIDFS_HOST = '127.0.0.1'
    GRIDFS_COLLECTION = 'my_collection'
    DEFAULT_FILE_STORAGE = 'mongo_storage.storage.GridFSStorage'

    If you don't want mongo storage to be your default, or if you
    want to change the settings for a particular model, create the
    storage object in your directly model.py file.

    models.py would look something like this:

    from django.db import models
    from mongo_storage.storage import GridFSStorage

    class MyModel(models.Model):
        content = models.FileField(upload_to="my_path",
                                   storage=GridFSStorage(collection="other_collection"))

    """
    default_host = 'localhost'
    default_port = 27017
    default_collection = 'fs'

    def __init__(self, host=None, port=None, collection=None):
        """
        For host, port and collection, we need to use the values
        given when present, otherwise use values from the settings
        file, or fall back to the defaults as a last resort.
        """
        host = host or getattr(settings, 'GRIDFS_HOST', self.default_host)
        port = port or getattr(settings, 'GRIDFS_PORT', self.default_port)
        collection = collection or getattr(settings, 'GRIDFS_COLLECTION', self.default_collection)

        self.db = Connection(host=host, port=port)[collection]
        self.fs = GridFS(self.db)

    def _save(self, name, content):
        """
        Django usually uses the file name as the text it stores and
        uses for subsequent lookups of the actual file. However,
        Mongo gives each file a unique ObjectId which is easier
        for us to lookup when querying Mongo directly. We'll give
        Django back the ObjectId to store instead of the file name.
        """
        oid = self.fs.put(content, filename=name)
        return str(oid)

    def _open(self, oid, *args, **kwars):
        return self.fs.get(ObjectId(oid))

    def delete(self, oid):
        self.fs.delete(ObjectId(oid))

    def exists(self, oid):
        """
        When Django first tries to save a file, it checks whether
        it exists using the file name. Because we are using ObjectIds
        instead of filenames, we know that a filename probably never
        a valid ObjectId and can assume it doesnt exist.
        """
        try:
            return self.fs.exists({'_id': ObjectId(oid)})
        except InvalidId:
            return False

    def size(self, oid):
        return self.fs.get(ObjectId(oid)).length

    def get_file_name(self, oid):
        return self.fs.get(ObjectId(oid)).filename

    def listdir(self, path):
        """
        according to GridFS documentation, this returns a list of
        every filename in this particular instance of GridFS.
        """
        return self.fs.list()

    def created_time(self, oid):
        return self.fs.get(ObjectId(oid)).upload_date
