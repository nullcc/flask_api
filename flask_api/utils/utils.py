import datetime


def to_dict(self):
    res = dict()
    for c in self.__table__.columns:
        if isinstance(getattr(self, c.name, None), datetime.datetime):
            res[c.name] = getattr(self, c.name, None).__str__()
        else:
            res[c.name] = getattr(self, c.name, None)
    return res
