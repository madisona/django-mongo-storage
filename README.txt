
A helper app for using MongoDB's GridFS as a storage backend for django.

mongo_storage contents include:

models.py
  - MongoFileMixin: a model mixin creating a MongoFileField called content
  - MongoDeleteFileMixin: a model mixin that will delete the underlying
    file when the model is deleted

fields.py
  - MongoFileField: a custom file field that gives you access to the
    file name through a 'file_name' property. Useful because the
    GridFSStorage makes Django store the MongoDB ObjectId instead
    of the file name.

storage.py
  - GridFSStorage: the Django storage module to interact with the pymongo,
    MongoDB's python adapters

admin.py
  - MongoFileAdminMixin: gives the ModelAdmin access to the stored
    file's file name and file size.
  - DeleteActionMixin: allows ModelAdmin to call the delete method on
    each model being deleted (so the underlying file will be delete
    also) when deleting items in bulk.

Dependencies:
  - mongodb Database
  - pymongo
  - django
