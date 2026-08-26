from src.user_api.dto.serializer.model_serializer import ModelSerializer as _serializer
serialize = _serializer.serialize
serialize_many = _serializer.serialize_many
required_relation = _serializer.required_relations


__all__ = [
    "serialize",
    "serialize_many",
    "required_relation",
]
