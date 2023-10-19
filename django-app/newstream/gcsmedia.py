from django.core.files.storage import default_storage
from django.http import FileResponse


def gcsmedia(request, path):
    fileobj = default_storage.open(path)
    return FileResponse(fileobj)