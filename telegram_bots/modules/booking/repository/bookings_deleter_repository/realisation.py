import typing


class BookigsDeleterRepository:
    def __init__(self) -> None:
        self.repo: typing.Dict[int, int] = {} # tg_id: booking id 

    def create(self, tg_id: int, data: int):
        self.repo[tg_id] = data
    
    def read(self, tg_id: int):
        if tg_id in self.repo:
            return self.repo[tg_id]

    def update(self, tg_id: int, data: int):
        self.repo[tg_id] = data

    def delete(self, tg_id: int):
        self.repo.pop(tg_id, None)
