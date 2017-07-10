# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import inspect
from flask_api.utils.database import CRUDMixin
from flask_api.database import Base
from flask_api.utils.utils import to_json_value
# from flask_api.db import transaction


class BaseModel(Base, CRUDMixin):

    __abstract__ = True

    @classmethod
    def select_columns(cls, results, col_names):
        """
        选择需要的列输出
        :param results:
        :param col_names:
        :return:
        """
        if results is None:
            return None

        mapper = inspect(cls)
        if isinstance(results, list):
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
        else:
            if not results:
                return dict()
            res = dict()
            if col_names == "*":
                for attr in mapper.attrs._data:
                    res[attr] = to_json_value(getattr(results, attr))
            else:
                for col_name in col_names:
                    res[col_name] = to_json_value(getattr(results, col_name))

            return res

    # @staticmethod
    # def session():
    #     return transaction.get_session()

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

    def update(self, data):
        """
        更新model
        :param data:
        :return:
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
