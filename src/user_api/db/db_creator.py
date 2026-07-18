import os.path
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.engine.base import Connection
from src.user_api.utils.JsonReadWrite import JsonReadWrite
from src.user_api.model.base_model import BaseModel


class _DatabaseAccount:
    def __init__(self):
        self.CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self._account_data_file = os.path.join(self.CURRENT_FILE_PATH, "database_account.json")
        self._id = ""
        self._pw = ""
        self._read_data()

    def _read_data(self) -> None:
        ac_data = JsonReadWrite.read(self._account_data_file)
        self._id = ac_data.get("id")
        self._pw = ac_data.get("pw")

    @property
    def id(self):
        return self._id

    @property
    def pw(self):
        return self._pw


class DatabaseCreator:
    # 새로 declarative_base()를 만들지 않고, 모든 모델이 상속받는
    # BaseModel(DeclarativeBase)을 그대로 재사용한다.
    # 이렇게 해야 UserModel, CategoryModel 등이 여기 metadata에 잡혀서
    # init_db()에서 실제로 테이블이 생성된다.
    Model = BaseModel

    _single_instance = None

    def __new__(cls):
        if cls._single_instance is None:
            cls._single_instance = super(DatabaseCreator, cls).__new__(cls)

        return cls._single_instance

    def __init__(self):
        cls = type(self)

        if not hasattr(cls, "_DatabaseCreator__init"):
            cls._DatabaseCreator__init = True
            self._database_account = _DatabaseAccount()
            self._engine = self._create_engine()
            self._session = self._create_session()
            self.init_db()

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine

    @staticmethod
    def create_object() -> "DatabaseCreator":
        return DatabaseCreator()

    def _create_all_tables(self, sync_connection: Connection) -> None:
        DatabaseCreator.Model.metadata.create_all(sync_connection)

    def _drop_all_tables(self, sync_connection: Connection) -> None:
        DatabaseCreator.Model.metadata.drop_all(sync_connection)


    def _create_engine(self) -> AsyncEngine:
        return create_async_engine(
            f"oracle-db-address",
            echo = False,
        )

    def _create_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind = self._engine,
            autoflush = False,
            expire_on_commit = False,
        )

    async def init_db(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(self._create_all_tables)

    async def drop_all_table(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(self._drop_all_tables)
