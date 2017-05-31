# -*- coding: utf-8 -*-

import datetime
import functools
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from Baicycle_API import application as app
from flask_api.utils.utils import to_json_value
from flask_api.config.config_dev import DevConfig

db_url = DevConfig.SQLALCHEMY_DATABASE_URI
engine = create_engine(db_url, encoding="utf-8", echo=True)
db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class BaseModel(object):

    @classmethod
    def select_columns(cls, results, col_names):
        """
        选择需要的列输出
        :param results:
        :param col_names:
        :return:
        """
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


def init_db():
    import flask_api.models
    Base.metadata.create_all(bind=engine)

