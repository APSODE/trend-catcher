from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import inspect, Identity


class BaseModel(DeclarativeBase):
    __abstract__ = True

    pk: Mapped[int] = mapped_column(Identity(start = 1, increment = 1), primary_key = True)

    def __repr__(self):
        table_keys = inspect(self.__class__).mapper.columns.keys()
        attrs = ', '.join(f"{key}={getattr(self, key)}" for key in table_keys)
        return f"{self.__tablename__}({attrs})"
