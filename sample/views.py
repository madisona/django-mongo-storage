# Create your views here.

import mimetypes

from django.http import HttpResponse
from django import shortcuts

from sample import models

def serve_mongo_download(request, mongo_id):
    obj = shortcuts.get_object_or_404(models.SampleModel, content=mongo_id)
    return get_mongo_response(obj.content)

def get_mongo_response(file_object, chunks=10000):
    """
    Prepares a Django HttpResponse to deliver the stored file.

    parameters:
     - file_object: the file object from our model's MongoFileField.
                    (ie. model.content in the sample models included)
     - chunks: how big of chunk size to read and deliver the file
    """
    mimetype, encoding = mimetypes.guess_type(file_object.file_name)
    mimetype = mimetype or 'application/octet-stream'

    response = HttpResponse(file_object.chunks(chunks), mimetype=mimetype)
    response['Content-Length'] = file_object.size
    response['Content-Disposition'] = "inline; filename = %s; " % file_object.file_name
    if encoding:
        response['Content-Encoding'] = encoding
    return response