class BookingViewerRepository:
    def __init__(self) -> None:
        self.repo = {} # tg_id: page_id

    def create(self, tg_id: int, page_id: int):
        self.repo[tg_id] = page_id
    
    def read(self, tg_id: int):
        if tg_id in self.repo:
            return self.repo[tg_id]

    def update(self, tg_id: int, page_id: int):
        self.repo[tg_id] = page_id

    def delete(self, tg_id: int):
        self.repo.pop(tg_id, None)
