from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class SerializerNotRegistered(AppException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, orm_class_name: str):
        super().__init__(
            f"No DTO registered for '{orm_class_name}'.",
            error_code = "INTERNAL_SERIALIZER_NOT_REGISTERED",
        )


class SerializerTypeMismatch(AppException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, expected_type_name: str):
        super().__init__(
            f"Expected '{expected_type_name}', but serialization produced a different type.",
            error_code = "INTERNAL_SERIALIZER_TYPE_MISMATCH",
        )


class UnexpectedNullSerializeTarget(AppException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self):
        super().__init__(
            "Cannot serialize a None instance.",
            error_code = "INTERNAL_SERIALIZE_TARGET_NULL",
        )
