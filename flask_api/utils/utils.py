
def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}