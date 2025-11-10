class DBClient(object):

    def __init__(self, db):
        self.engine = db
        self.session = db.session

    def _apply_filters(self, stmt, table, **kwargs):
        """
        Build a SQLAlchemy query when additional parameters are needed
        """
        filters = []
        for key, val in kwargs.items():
            # Filters are made from kwarg key: value pairs. This
            # only works for single table filtering (no joins).
            # For the given table, get the key from the kwarg and create a
            # .where() filter for that particular key to append
            # to the select statement.

            filters.append(getattr(table, key) == val)

        if filters:
            stmt = stmt.where(*filters)

        return stmt

    def _query(self, stmt):
        return self.session.scalars(stmt)

    def create(self, table, **kwargs):
        pass

    def get(self, table, **kwargs):
        if not kwargs:
            query = self._query(self.engine.select(table))
        else:
            filtered_query = self._apply_filters(
                self.engine.select(table), table, **kwargs
            )
            query = self._query(filtered_query)

        return query

    def get_with_join(self, table, **kwargs):
        pass

    def update(self, table, **kwargs):
        pass

    def delete(self, table, **kwargs):
        pass

    def filter(self, table, search_term, join, **kwargs):
        pass
