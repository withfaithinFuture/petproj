import sqlalchemy as sa
from uuid import UUID, uuid4
from sqlalchemy.orm import DeclarativeMeta, Mapped, declarative_base, mapped_column

metadata = sa.MetaData()


class BaseServiceModel:
    """Базовый класс для таблиц сервиса."""

    @classmethod
    def on_conflict_constraint(cls) -> tuple | None:
        return None

                                        #привязка            #добавл каст методов
Base: DeclarativeMeta = declarative_base(metadata=metadata, cls=BaseServiceModel)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(sa.String())
