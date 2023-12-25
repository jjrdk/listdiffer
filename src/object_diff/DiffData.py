class DiffData:
    def __init__(self, data: list[int]):
        self.data: list[int] = data
        self.len: int = len(data)
        self.modified: list[bool] = [False] * (self.len + 2)
