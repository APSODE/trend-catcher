from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import inspect

class BaseModel(DeclarativeBase):
    __tablename__ = "[dev]BaseModel"
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)

    def __repr__(self):
        table_keys = inspect(self.__class__).mapper.columns.keys()
        attrs = ', '.join(f"{key}={getattr(self, key)}" for key in table_keys)
        return f"{self.__tablename__}({attrs})"













