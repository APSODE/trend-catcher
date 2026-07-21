from fastapi import status

class SNSError(Exception):
    status_code: int = 400

class NotFoundError(SNSError):
    status_code = status.HTTP_404_NOT_FOUND

class DispatchError(SNSError):
    status_code = status.HTTP_502_BAD_GATEWAY