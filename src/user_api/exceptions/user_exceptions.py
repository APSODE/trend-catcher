class InvalidNameException(Exception):
    def __init__(self, name: str, max_length: int):
        super().__init__(f"Invalid name length. Expected {max_length} characters, but received {len(name)}.")
        
        
        