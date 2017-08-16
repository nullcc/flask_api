# -*- coding: utf-8 -*-

from flask_jsonrpc.proxy import ServiceProxy


class BaseService(object):

    """
    服务基类
    """

    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.server = ServiceProxy("{}/{}".format(self.url, self.name))

    @staticmethod
    def parse_response(response):
        result = response["result"]
        if result["success"] == False:
            raise Exception(result["message"])
        return result["data"]
