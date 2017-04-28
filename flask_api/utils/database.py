import pytz
from flask_api.extensions import db
from flask_api.utils.signals import model_saved
from flask import current_app as app


class CRUDMixin(object):
    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def save(self):
        """
        保存对象到数据库
        :return:
        """
        db.session.add(self)
        db.session.commit()
        model_saved.send(app._get_current_object())
        # db.session.close()
        return self

    def delete(self):
        """
        从数据库中删除对象
        :return:
        """
        db.session.delete(self)
        db.session.commit()
        return self


class UTCDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        """Way into the database."""
        if value is not None:
            # store naive datetime for sqlite and mysql
            if dialect.name in ("sqlite", "mysql"):
                return value.replace(tzinfo=None)

            return value.astimezone(pytz.UTC)

    def process_result_value(self, value, dialect):
        """Way out of the database."""
        # convert naive datetime to non naive datetime
        if dialect.name in ("sqlite", "mysql") and value is not None:
            return value.replace(tzinfo=pytz.UTC)

        # other dialects are already non-naive
        return value
