from .base import Base


class Video(Base):
    def __init__(self, id, cache, session):
        super().__init__(id, cache, session)

    def _build_url(self):
        pass

