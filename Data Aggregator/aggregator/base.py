

class DataAggregator:
    def __init__(self, primary_source, secondary_sources):
        self.primary_sources = primary_source
        self.secondary_sources = secondary_sources


    def aggregate(self):

        aggregated_data = {}

        for data in self.primary_sources.fetch_data():
            id = data.get("id")
            aggregated_data[id] = data

        for source in self.secondary_sources:
            for data in source.fetch_data():
                id = data.get("id")
                if id in aggregated_data:
                    aggregated_data[id].update(data)
                else: print(f"No data found for source {id} in {source}")

        return aggregated_data