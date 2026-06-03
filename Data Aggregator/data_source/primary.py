from .data_source import DataSource

class PrimaryDataSource(DataSource):

    def fetch_data(self):
        return [
            {"id": "1", "name": "Alice", "email": "alice@example.com"},
            {"id": "2", "name": "Bob", "email": "bob@example.com"}
        ]