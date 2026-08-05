from src.user_api.dto.model_serializer import ModelSerializer as _serializer

serialize = _serializer.serialize
serialize_many = _serializer.serialize_many

__all__ = [
    "serialize",
    "serialize_many"
]