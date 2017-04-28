#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random


def to_dict(self):
    """
    把对象转换成dict
    :param self:
    :return:
    """
    res = dict()
    for c in self.__table__.columns:
        if isinstance(getattr(self, c.name, None), datetime.datetime):
            res[c.name] = getattr(self, c.name, None).__str__()
        else:
            res[c.name] = getattr(self, c.name, None)
    return res


# 生成指定长度的0-9串
def gen_random_number_string(key_len):
    key_list = [random.choice("0123456789") for i in range(key_len)]
    return "".join(key_list)
