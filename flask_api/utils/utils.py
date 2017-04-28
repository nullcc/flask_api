#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


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
