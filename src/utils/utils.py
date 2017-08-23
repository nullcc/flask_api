#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random
from sqlalchemy import inspect


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
        elif isinstance(getattr(self, c.name, None), bytes):
            res[c.name] = bool(getattr(self, c.name, None))
        else:
            res[c.name] = getattr(self, c.name, None)
    return res


def to_json_value(value):
    if isinstance(value, datetime.datetime):
        return value.__str__()
    elif isinstance(value, bytes):
        return bool(value)
    else:
        return value


def filter_columns(cls, results, col_names):
    mapper = inspect(cls)
    res = []
    for element in results:
        data = dict()
        if col_names == "*":
            for attr in mapper.attrs._data:
                data[attr] = to_json_value(getattr(element, attr))
        else:
            for col_name in col_names:
                data[col_name] = to_json_value(getattr(element, col_name))
        res.append(data)
    return res


# 生成指定长度的0-9串
def gen_random_number_string(key_len):
    key_list = [random.choice("0123456789") for i in range(key_len)]
    return "".join(key_list)
