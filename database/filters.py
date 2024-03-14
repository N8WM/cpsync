import json
from typing import Any
from database.setup import DB


class Filter:
    """Filter functions"""

    def __init__(self, database: DB) -> None:
        self.client = database.client
        self.db = database.db

    def filter(self, collection_name: str, filter: str) -> str:
        """
        Filter a collection by a MongoDB JSON document

        :param collection_name: the name of the collection to filter
        :param filter: the filter to apply, must be a valid MongoDB JSON document

        :return: a list of documents that match the filter, as a JSON string
        """
        filter = json.loads(filter)
        result = self.db[collection_name].find(filter)
        return json.dumps(list(result))
