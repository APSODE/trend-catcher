from typing import Any, Callable, Dict, List, Sequence, Type, TypeVar, Union

from pydantic import BaseModel as _PydanticModel
from sqlalchemy.orm import InstrumentedAttribute

from src.user_api.exceptions.internal_exceptions import (
    SerializerNotRegistered,
    SerializerTypeMismatch,
    UnexpectedNullSerializeTarget,
)
from src.user_api.model import BaseModel as _ORMBaseModel

_ORM = TypeVar("_ORM", bound = _ORMBaseModel)
_DTO = TypeVar("_DTO", bound = _PydanticModel)

FieldTransformer = Callable[[Any], Any]
RelationPath = Union[InstrumentedAttribute, Sequence[InstrumentedAttribute]]


class ModelSerializer:
    _registry: Dict[Type[_ORMBaseModel], List[Type[_PydanticModel]]] = {}
    _field_transformers: Dict[Type[_PydanticModel], Dict[str, FieldTransformer]] = {}
    _relations: Dict[Type[_PydanticModel], List[RelationPath]] = {}

    _pending_transformers: Dict[Type[_PydanticModel], Dict[str, FieldTransformer]] = {}
    _pending_relations: Dict[Type[_PydanticModel], List[RelationPath]] = {}

    @staticmethod
    def _resolve_relation_chain(instance: _ORMBaseModel, *attribute_names: str) -> List[_ORMBaseModel]:
        current: List[_ORMBaseModel] = [instance]

        for attribute_name in attribute_names:
            next_level: List[_ORMBaseModel] = []

            for obj in current:
                value = getattr(obj, attribute_name)

                if isinstance(value, list):
                    next_level.extend(value)
                elif value is not None:
                    next_level.append(value)

            current = next_level

        return current

    @classmethod
    def relation(cls, field_name: str, *path: InstrumentedAttribute, to: Type[_DTO]):
        def decorator(dto_class: Type[_DTO]) -> Type[_DTO]:
            attribute_names = tuple(attribute.key for attribute in path)

            def _transformer(instance: _ORMBaseModel) -> List[_DTO]:
                related_instances = cls._resolve_relation_chain(instance, *attribute_names)
                return cls.serialize_many(related_instances, to)

            cls._pending_transformers.setdefault(dto_class, {})[field_name] = _transformer

            relation_path: RelationPath = path[0] if len(path) == 1 else path
            cls._pending_relations.setdefault(dto_class, []).append(relation_path)

            return dto_class
        return decorator

    @classmethod
    def bind_model(cls, *orm_classes: Type[_ORM]):
        def decorator(dto_class: Type[_DTO]) -> Type[_DTO]:
            for orm_class in orm_classes:
                cls._registry.setdefault(orm_class, []).append(dto_class)

            pending_transformers = cls._pending_transformers.get(dto_class)
            if pending_transformers:
                cls._field_transformers[dto_class] = pending_transformers

            pending_relations = cls._pending_relations.get(dto_class)
            if pending_relations:
                cls._relations[dto_class] = pending_relations

            return dto_class

        return decorator

    @classmethod
    def required_relations(cls, dto_class: Type[_PydanticModel]) -> List[RelationPath]:
        return cls._relations.get(dto_class, [])

    @classmethod
    def serialize(cls, instance: _ORM, expected_type: Type[_DTO]) -> _DTO:
        if instance is None:
            raise UnexpectedNullSerializeTarget()

        orm_class = type(instance)
        dto_classes = cls._registry.get(orm_class, [])

        if expected_type not in dto_classes:
            raise SerializerNotRegistered(orm_class_name = orm_class.__name__)

        transformers = cls._field_transformers.get(orm_class, {})

        if not transformers:
            result = expected_type.model_validate(instance)
        else:
            data = {}
            # expected_type 자체가 Pydantic.BaseModel의 하위 타입이기에
            # 공변성이 성립함 -> 경고가 무시되어 있으나 타입체커의 오진이니 안전함
            for field_name in expected_type.model_fields:  # type: ignore[attr-defined]
                if field_name in transformers:
                    data[field_name] = transformers[field_name](instance)
                else:
                    data[field_name] = getattr(instance, field_name)
            result = expected_type.model_validate(data)

        if not isinstance(result, expected_type):
            raise SerializerTypeMismatch(expected_type_name = expected_type.__name__)

        return result

    @classmethod
    def serialize_many(cls, instances: List[_ORM], expected_type: Type[_DTO]) -> List[_DTO]:
        return [cls.serialize(instance, expected_type) for instance in instances]
