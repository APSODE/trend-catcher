from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData, Identity, Text
from sqlalchemy.types import TypeDecorator
from typing import Any
import json

#디버깅이나 제약조건 관리 등에서 쉽게 확인할 수 있게 이름에 적용시킬 컨벤션을 정의, 모든 모델에 통일적용
NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s", #기본키, pk_테이블명
    "fk": "fk_%(table_name)s_%(column_0_name)s", #외래키, fk_테이블명_컬럼명
    "ix": "idx_%(table_name)s_%(column_0_name)s", #인덱스, idx_테이블명_컬럼명
    "uq": "uq_%(table_name)s_%(column_0_name)s", #유일성, uq_테이블명_컬럼명
    "ck": "ck_%(table_name)s_%(constraint_name)s" #제약성 체크, ck_테이블명_제약명
}

class AbstractBaseModel(DeclarativeBase):
    __abstract__ = True #이거 실체 없음
    metadata = MetaData(naming_convention = NAMING_CONVENTION) #컨벤션 적용
    pk: Mapped[int] = mapped_column(Identity(start = 1, increment = 1), primary_key = True) #기본키

#오라클에 json들어가면 터지는거 방지
class JsonType(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value: Any, dialect) -> str | None:
        if value is None:
            return None
        else:
            return json.dumps(value, ensure_ascii = False)

    def process_result_value(self, value: str | None, dialect) -> Any:
        if value is None:
            return None
        else:
            return json.loads(value)
