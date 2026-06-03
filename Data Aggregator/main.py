import json

from aggregator.base import DataAggregator
from data_source import PrimaryDataSource, Secondary1DataSource, Secondary2DataSource

if __name__ == "__main__":

    primary_data_source = PrimaryDataSource()
    secondary_data_sources = [Secondary1DataSource(), Secondary2DataSource()]
    data  = DataAggregator(primary_source=primary_data_source, secondary_sources=secondary_data_sources).aggregate()

    print(json.dumps(data, indent=4))

    print(f"Aggregated data: {data}")