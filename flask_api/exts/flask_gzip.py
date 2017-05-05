import gzip
from flask import request


class Gzip(object):
    def __init__(self, app=None, compress_level=6):
        self.compress_level = compress_level
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.after_request(self.after_request)

    def after_request(self, response):
        accept_encoding = request.headers.get('Accept-Encoding', '')
        if not accept_encoding:
            return response

        encodings = accept_encoding.split(',')
        if 'gzip' not in encodings:
            return response

        if (200 > response.status_code >= 300) or len(response.data) < 500 or 'Content-Encoding' in response.headers:
            return response

        response.data = gzip.compress(response.data, compresslevel=self.compress_level)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(response.data)

        return response
