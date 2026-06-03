from .data_source import DataSource

class Secondary2DataSource(DataSource):

    def fetch_data(self):
        return [
            {"id": "1", "tickets_count": 2},
            {"id": "3", "tickets_count": 5}
        ]