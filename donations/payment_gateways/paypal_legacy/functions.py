import json
import time
import pycurl
import certifi
from io import BytesIO

from newstream.functions import _debug


def curlPaypalIPN(url, headers, post_data=''):
    _debug('curlPaypalIPN url: {}'.format(url))
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_1_1)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.HTTPHEADER, headers)
    c.setopt(c.FORBID_REUSE, 1)
    c.setopt(c.POST, 1)
    if post_data:
        c.setopt(c.POSTFIELDS, post_data)
    c.setopt(c.VERBOSE, True)
    c.perform()
    status_code = c.getinfo(pycurl.HTTP_CODE)
    c.close()

    body = buffer.getvalue()
    # Body is a byte string.
    # We have to know the encoding in order to print it to a text file
    # such as standard output.
    if status_code >= 300:
        raise RuntimeError("curlPaypalipN request unsuccessful. Status Code: {}, Full body: {}".format(status_code, body.decode('utf-8')))
    # print("Curl to PayPal status code: {}({})".format(status_code, type(status_code)))
    # Here we deserialize the json into a python object
    # _debug('Success! curlPaypalIPN body: {}'.format(body.decode('utf-8')))
    return body.decode('utf-8')