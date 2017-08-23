# -*- coding: utf-8 -*-

from .base import BaseService
from .utils import after_action


class MessageService(BaseService):

    def __init__(self, url, name):
        super(MessageService, self).__init__(url, name)

    @after_action(BaseService.parse_response)
    def send_login_sms(self, telephone, code):
        return self.server.MessageService.send_login_sms(telephone, code)
