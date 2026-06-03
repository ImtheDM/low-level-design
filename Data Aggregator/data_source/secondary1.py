from .data_source import DataSource

class Secondary1DataSource(DataSource):

    def fetch_data(self):
        return [
            {"id": "1", "tier": "Premium", "newsletter": True},
            {"id": "2", "tier": "Free"}
        ]