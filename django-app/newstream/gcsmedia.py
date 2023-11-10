import logging
logger = logging.getLogger('newstream')
from django.core.files.storage import default_storage
from django.http import FileResponse, HttpResponse


def gcsmedia(request, path):
    try:
        fileobj = default_storage.open(path)
        return FileResponse(fileobj)
    except FileNotFoundError:
        return HttpResponse(status=404)
