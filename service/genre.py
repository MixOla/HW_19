from dao.genre import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, genre_id):
        return self.dao.create(genre_id)

    def update(self, genre_id):
        self.dao.update(genre_id)
        return self.dao

    def delete(self, genre_id):
        self.dao.delete(genre_id)
