import json
from typing import Any
from database.contexts.database import DB


class Functions:
    """Functions context for LLM function calling"""

    def __init__(self, database: DB) -> None:
        self.client = database.client
        self.db = database.db

    def filter(self, collection_name: str, filter: str) -> list[dict[str, Any]]:
        """
        Filter a collection by a MongoDB JSON document

        :param collection_name: the name of the collection to filter
        :param filter: the filter to apply, must be a valid MongoDB JSON document

        :return: a list of documents that match the filter
        """
        filter_doc = json.loads(filter)
        result = self.db[collection_name].find(filter_doc)
        return list(result)

    def aggregate(self, collection_name: str, pipeline: str) -> list[dict[str, Any]]:
        """
        Run an aggregation pipeline given a pipeline and a collection name.

        :param collection_name: the name of the collection to aggregate
        :param pipeline: the pipeline to apply, must be a valid MongoDB JSON document

        :return: a list of documents that match the pipeline
        """
        pipeline_doc = json.loads(pipeline)
        result = self.db[collection_name].aggregate(pipeline_doc)
        return list(result)
