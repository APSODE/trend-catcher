# NOTE: 이 파일은 제공된 문서 목록에 원본이 포함되어 있지 않아
# src/user_api/dto/serializer/model_serializer.py의 ModelSerializer.bind_model / relation
# 사용 패턴을 근거로 재구성한 파일입니다. 실제 프로젝트의 원본 내용과 다를 수 있으니
# 반드시 원본과 비교 후 사용해주세요.
from src.user_api.dto.serializer.model_serializer import ModelSerializer as _serializer

bind_model = _serializer.bind_model
relation = _serializer.relation

__all__ = [
    "bind_model",
    "relation",
]
