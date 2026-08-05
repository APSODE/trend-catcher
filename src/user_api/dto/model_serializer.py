from typing import Dict, List, Type, TypeVar

from pydantic import BaseModel as _PydanticModel

from src.user_api.model.base_model import BaseModel as _ORMBaseModel

_ORM = TypeVar("_ORM", bound = _ORMBaseModel)
_DTO = TypeVar("_DTO", bound = _PydanticModel)


class ModelSerializer:
    _registry: Dict[type, Type[_PydanticModel]] = {}

    @classmethod
    def bind_model(cls, orm_class: Type[_ORM]):
        def decorator(dto_class: Type[_DTO]) -> Type[_DTO]:
            cls._registry[orm_class] = dto_class
            return dto_class
        return decorator

    @classmethod
    def serialize(cls, instance: _ORM, expected_type: Type[_DTO]) -> _DTO:
        dto_class = cls._registry.get(type(instance))

        if dto_class is None:
            raise ValueError(f"No DTO registered for '{type(instance).__name__}'.")

        result = dto_class.model_validate(instance)

        if not isinstance(result, expected_type):
            raise TypeError(
               f"Expected '{expected_type.__name__}', "
               f"but the registered DTO for '{type(instance).__name__}' is '{dto_class.__name__}'."
            )

        return result

    @classmethod
    def serialize_many(cls, instances: List[_ORM], expected_type: Type[_DTO]) -> List[_DTO]:
        return [cls.serialize(instance, expected_type) for instance in instances]