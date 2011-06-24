
from django.db import models

from mongo_storage.fields import MongoFileField

__all__ = ('MongoDeleteFileMixin', 'MongoFileMixin')

class MongoDeleteFileMixin(models.Model):
    """
    Will delete the file from the database when the model
    is deleted.

    This could potentially lead to a couple issues, so make sure
    you're comfortable with them before actually using this.

    - the delete could succeed from the file system, but not succeed
      in Django. You would be left with a lost file.

    - if multiple items are pointing to the same exact file, this may
      cause the not-deleted file to lose the file it was pointing to.
    """

    content = MongoFileField(upload_to="files")

    class Meta(object):
        abstract = True

    def delete(self, using=None):
        self.content.delete()
        super(MongoDeleteFileMixin, self).delete(using=using)

class MongoFileMixin(models.Model):
    content = MongoFileField(upload_to="files")

    class Meta(object):
        abstract = True
    