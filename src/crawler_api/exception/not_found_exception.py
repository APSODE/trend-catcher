class NotFoundException(Exception):
    def __init__(self, message : str | None = None):
        self.status_code = 404
        if message:
            super().__init__(message)
        else:
            super().__init__("데이터를 찾지 못했습니다")
