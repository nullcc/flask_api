# -*- coding: utf-8 -*-

from .base import BaseService
from .utils import after_action


class UserService(BaseService):

    def __init__(self, url, name):
        super(UserService, self).__init__(url, name)

    @after_action(BaseService.parse_response)
    def register_user(self, id_card_no, deposit, balance, credit_score, real_name, telephone):
        return self.server.UserService.register_user(id_card_no,
                                                     deposit,
                                                     balance,
                                                     credit_score,
                                                     real_name,
                                                     telephone)

