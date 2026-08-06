from typing import Any, Callable, Dict, List, Sequence, Type, TypeVar, Union

from pydantic import BaseModel as _PydanticModel
from sqlalchemy.orm import InstrumentedAttribute

from src.user_api.model import BaseModel as _ORMBaseModel

_ORM = TypeVar("_ORM", bound = _ORMBaseModel)
_DTO = TypeVar("_DTO", bound = _PydanticModel)

FieldTransformer = Callable[[Any], Any]
RelationPath = Union[InstrumentedAttribute, Sequence[InstrumentedAttribute]]


class ModelSerializer:
    _registry: Dict[type, Type[_PydanticModel]] = {}
    _field_transformers: Dict[type, Dict[str, FieldTransformer]] = {}
    _relations: Dict[type, List[RelationPath]] = {}

    _pending_transformers: Dict[type, Dict[str, FieldTransformer]] = {}
    _pending_relations: Dict[type, List[RelationPath]] = {}

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
    def bind_model(cls, orm_class: Type[_ORM]):
        def decorator(dto_class: Type[_DTO]) -> Type[_DTO]:
            cls._registry[orm_class] = dto_class

            pending_transformers = cls._pending_transformers.pop(dto_class, None)
            if pending_transformers:
                cls._field_transformers[orm_class] = pending_transformers

            pending_relations = cls._pending_relations.pop(dto_class, None)
            if pending_relations:
                cls._relations[orm_class] = pending_relations

            return dto_class
        return decorator

    @classmethod
    def required_relations(cls, orm_class: type) -> List[RelationPath]:
        return cls._relations.get(orm_class, [])

    @classmethod
    def serialize(cls, instance: _ORM, expected_type: Type[_DTO]) -> _DTO:
        orm_class = type(instance)
        dto_class = cls._registry.get(orm_class)

        if dto_class is None:
            raise ValueError(f"No DTO registered for '{orm_class.__name__}'.")

        transformers = cls._field_transformers.get(orm_class, {})

        if not transformers:
            result = dto_class.model_validate(instance)
        else:
            data = {}
            for field_name in dto_class.model_fields:
                if field_name in transformers:
                    data[field_name] = transformers[field_name](instance)
                else:
                    data[field_name] = getattr(instance, field_name)
            result = dto_class.model_validate(data)

        if not isinstance(result, expected_type):
            raise TypeError(
                f"Expected '{expected_type.__name__}', "
                f"but the registered DTO for '{orm_class.__name__}' is '{dto_class.__name__}'."
            )
        return result

    @classmethod
    def serialize_many(cls, instances: List[_ORM], expected_type: Type[_DTO]) -> List[_DTO]:
        return [cls.serialize(instance, expected_type) for instance in instances]