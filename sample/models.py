from django.db import models

from mongo_storage.models import MongoFileMixin, MongoDeleteFileMixin



class SampleModel(MongoFileMixin):
    """
    Sample model using MongoDB as a storage backend.
    """
    display_name = models.CharField(max_length=100)

    @models.permalink
    def get_absolute_url(self):
        return ('sample:download_file', (self.content.name,))


class SampleDeleteModel(MongoDeleteFileMixin):
    """
    Sample model that will delete the uploaded file
    when the model gets deleted.
    """
    display_name = models.CharField(max_length=100)
