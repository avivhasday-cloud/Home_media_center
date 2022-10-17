import logging
from itertools import islice
from typing import Union, List

import pymongo


class GenericMongoDB:

    _ID_KEY_FIELD = "_id"
    INCLUDE_OPERATION = "$in"
    SET_OPERATION = "$set"
    MATCH_OPERATION = "$match"
    SORT_OPERATION = "$sort"
    LIMIT_OPERATION = "$limit"

    @staticmethod
    def is_document_already_exists(field: str, keyword_to_filter: str, collection: pymongo.collection.Collection) -> bool:
        res = GenericMongoDB._query_single_document_from_collection(field, keyword_to_filter, collection)
        return True if res else False

    @staticmethod
    def insert_documents_to_collection(documents_to_insert: [dict], collection: pymongo.collection.Collection) -> [str]:
        res = collection.insert_many(documents_to_insert)
        return res.inserted_ids if res else None

    @staticmethod
    def update_document_in_collection(document_id: str, new_document_values: dict, collection: pymongo.collection.Collection) -> bool:
        res = collection.update_one(
            {GenericMongoDB._ID_KEY_FIELD: document_id},
            {GenericMongoDB.SET_OPERATION: new_document_values},
            upsert=False
        )
        return True if res.matched_count > 0 else False

    @staticmethod
    def delete_documents_from_collection(documents_ids_to_remove: [str], collection: pymongo.collection.Collection):
        res = collection.delete_many({GenericMongoDB._ID_KEY_FIELD: {GenericMongoDB.INCLUDE_OPERATION: documents_ids_to_remove}})
        return True if res.deleted_count == len(documents_ids_to_remove) else False

    @staticmethod
    def query_documents_from_collection(field_to_filter: str, filter_by: Union[str, List], collection: pymongo.collection.Collection, sort_by: Union[dict, int] = 1, limit_count: int = 1000):
        doc_list = list()
        if isinstance(filter_by, str):
            document = GenericMongoDB._query_single_document_from_collection(field_to_filter, filter_by, collection)
            doc_list.append(document)
        else:
            iterator = iter(filter_by)
            while filter_by_chunked := list(islice(iterator, limit_count)):
                documents = GenericMongoDB._query_many_documents_from_collection(field_to_filter, filter_by_chunked, collection, sort_by, limit_count)
                doc_list.extend(documents)
        return doc_list

    @staticmethod
    def _query_single_document_from_collection(field: str, keyword_to_filter: str, collection: pymongo.collection.Collection):
        document = collection.find_one({field: keyword_to_filter})
        return document if document else None

    @staticmethod
    def _query_many_documents_from_collection(field_to_filter: str, filter_by: Union[str, List], collection: pymongo.collection.Collection, sort_by: Union[dict, int], limit_count: int):
        pipeline = [
            {
                GenericMongoDB.MATCH_OPERATION: {field_to_filter: filter_by}
            },
            {
                GenericMongoDB.SORT_OPERATION: sort_by
            },
            {
                GenericMongoDB.LIMIT_OPERATION: limit_count
            }
        ]
        res = collection.aggregate(pipeline)
        return res if res else list()


class MongoHandler:

    def __init__(self, mongo_server_ip: str, database_name: str, port: int = 27017, logger: logging.Logger = logging.Logger):
        self.client = pymongo.MongoClient(mongo_server_ip, port)
        self.db = self.client.get_database(database_name)
        self.logger = logger

