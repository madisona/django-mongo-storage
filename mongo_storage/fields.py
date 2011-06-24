
"""
When GridFSStorage saves a file, it is giving Django back
the ObjectId, not the file name. Sometimes it is nice to
know the file name. Using the MongoFileField instead of
Django's regular FileField you can access the file name.

Sample usage:

class MyModel(models.Model):
    content = MongoFileField(upload_to="my_location")

# a sample to list all the file names of your saved files
for obj in MyModel.objects.all()
    print obj.content.file_name


"""

import os

from django.db import models

__all__ = ('MongoFileField',)

class MongoFieldFile(models.fields.files.FieldFile):

    @property
    def file_name(self):
        storage_name = self.storage.get_file_name(self.name)
        return os.path.basename(storage_name)

class MongoFileField(models.FileField):
    attr_class = MongoFieldFile

    
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^mongo_storage\.fields\.MongoFileField"])
except ImportError:
    pass