from typing import Dict, List, Type, TypeVar, Callable, Any

from pydantic import BaseModel as _PydanticModel

from src.user_api.model.base_model import BaseModel as _ORMBaseModel

_ORM = TypeVar("_ORM", bound = _ORMBaseModel)
_DTO = TypeVar("_DTO", bound = _PydanticModel)


FieldTransformer = Callable[[Any], Any]

class ModelSerializer:
    _registry: Dict[type, Type[_PydanticModel]] = {}
    _field_transformers: Dict[type, Dict[str, FieldTransformer]] = {}

    @classmethod
    def bind_model(cls, orm_class: Type[_ORM], **transformers: FieldTransformer):
        def decorator(dto_class: Type[_DTO]) -> Type[_DTO]:
            cls._registry[orm_class] = dto_class
            if transformers:
                cls._field_transformers[orm_class] = transformers
            return dto_class
        return decorator

    @classmethod
    def serialize(cls, instance: _ORM, expected_type: Type[_DTO]) -> _DTO:
        orm_class = type(instance)
        dto_class = cls._registry.get(type(instance))

        if dto_class is None:
            raise ValueError(f"No DTO registered for '{type(instance).__name__}'.")

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
               f"but the registered DTO for '{type(instance).__name__}' is '{dto_class.__name__}'."
            )

        return result

    @classmethod
    def serialize_many(cls, instances: List[_ORM], expected_type: Type[_DTO]) -> List[_DTO]:
        return [cls.serialize(instance, expected_type) for instance in instances]