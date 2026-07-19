class ParsingFailException(Exception):
    def __init__(self, message : str | None = None):
        self.status_code = 404
        if message:
            super().__init__("파싱 과정에서 문제가 발생했습니다\n"+message)
        else:
            super().__init__("파싱 과정에서 문제가 발생했습니다")
