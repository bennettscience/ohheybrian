from datetime import datetime


class DBClient(object):

    def __init__(self, db):
        self.engine = db
        self.session = db.session

    def build_db_query(self, table, **kwargs):
        """
        Build a SQLAlchemy query when additional parameters are needed
        """
        stmt = ""
        for key, val in kwargs.items():
            stmt += f".where({table}.{key} == {val})"

        return stmt

    def _query(self, stmt):
        return self.session.execute(stmt)

    def create(self, table, **kwargs):
        pass

    def get(self, table, **kwargs):
        stmt = self.build_db_query(table, **kwargs)
        print(stmt)
        return self._query(self.engine.select(table) + stmt)

    def update(self, table, **kwargs):
        pass

    def delete(self, table, **kwargs):
        pass

    def filter(self, table, search_term, join, **kwargs):
        pass
