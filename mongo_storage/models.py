
from django.db import models

from mongo_storage.fields import MongoFileField

__all__ = (
    'DeleteFileMixin',
    'MongoDeleteFileModel', 'MongoFileModel',
)

class DeleteFileMixin(object):
    """
    Will delete the file from the database when the model
    is deleted. The file field MUST be named 'content'.

    This could potentially lead to a couple issues, so make sure
    you're comfortable with them before actually using this.

    - the delete could succeed from the file system, but not succeed
      in Django. You would be left with a lost file.

    - if multiple items are pointing to the same exact file, this may
      cause the not-deleted file to lose the file it was pointing to.
    """

    def delete(self, using=None):
        self.content.delete()
        super(DeleteFileMixin, self).delete(using=using)


class MongoFileModel(models.Model):
    content = MongoFileField(upload_to="files")

    class Meta(object):
        abstract = True

class MongoDeleteFileModel(DeleteFileMixin, MongoFileModel):

    class Meta(object):
        abstract = True
