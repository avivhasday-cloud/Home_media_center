import logging
from itertools import islice
from typing import Union, List

import pymongo

from assets.movie import Movie


class MongoFields:
    ID_KEY_FIELD = "_id"
    INCLUDE_OPERATION = "$in"
    SET_OPERATION = "$set"
    MATCH_OPERATION = "$match"
    SORT_OPERATION = "$sort"
    LIMIT_OPERATION = "$limit"
    ALL_EXISTS_DOCS = {"$exists": True}


class GenericMongoDB:



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
            {MongoFields.ID_KEY_FIELD: document_id},
            {MongoFields.SET_OPERATION: new_document_values},
            upsert=False
        )
        return True if res.matched_count > 0 else False

    @staticmethod
    def delete_documents_from_collection(documents_ids_to_remove: [str], collection: pymongo.collection.Collection) -> int:
        res = collection.delete_many({MongoFields.ID_KEY_FIELD: {MongoFields.INCLUDE_OPERATION: documents_ids_to_remove}})
        return res.deleted_count if res else None

    @staticmethod
    def query_documents_from_collection(field_to_filter: str, filter_by: Union[str, List, dict], collection: pymongo.collection.Collection, sort_by: Union[dict, int] = 1, limit_count: int = 1000):
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
    def _query_many_documents_from_collection(field_to_filter: str, filter_by: Union[str, List, dict], collection: pymongo.collection.Collection, sort_by: Union[dict, int], limit_count: int):
        pipeline = [
            {
                MongoFields.MATCH_OPERATION: {field_to_filter: filter_by}
            },
            {
                MongoFields.SORT_OPERATION: sort_by
            },
            {
                MongoFields.LIMIT_OPERATION: limit_count
            }
        ]
        res = collection.aggregate(pipeline)
        return res if res else list()


class MongoHandler(GenericMongoDB):

    def __init__(self, mongo_server_ip: str, database_name: str, port: int = 27017, logger: logging.Logger = logging.Logger):
        self.client = pymongo.MongoClient(mongo_server_ip, port)
        self.db = self.client.get_database(database_name)
        self.logger = logger

    def get_filtered_list_of_documents_to_insert_to_collection(self, documents_list: [dict], collection: pymongo.collection.Collection) -> [dict]:
        documents_names_in_db = [doc["name"] for doc in documents_list if MongoHandler.is_document_already_exists("name", doc["name"], collection)]
        self.logger.info(f"There are {len(documents_names_in_db)}/{len(documents_list)} documents that already exists in DB, Filtering documents list to insert!")
        filtered_docs = list(filter(lambda x: x["name"] not in documents_names_in_db, documents_list))
        return filtered_docs


    def get_movies(self, list_of_ids: [str] = None, list_of_names: [str] = None, sort_by: Union[dict, int] = 1, limit: int = 1000) -> [Movie]:
        if list_of_ids is not None:
            documents = MongoHandler.query_documents_from_collection(MongoFields.ID_KEY_FIELD, list_of_ids, self.db.movie, sort_by, limit)
        elif list_of_names is not None:
            documents = MongoHandler.query_documents_from_collection("name", list_of_names, self.db.movie, sort_by, limit)
        else:
            documents = MongoHandler.query_documents_from_collection(MongoFields.ID_KEY_FIELD, MongoFields.ALL_EXISTS_DOCS, self.db.movie, sort_by, limit)

        return [Movie(**doc) for doc in documents]

    def update_movie(self, movie_id: str, new_movie_details: dict):
        res = MongoHandler.update_document_in_collection(movie_id, new_movie_details, self.db.movie)
        if not res:
            raise RuntimeError(f"Failed to update movie {movie_id}")
        return True

    def insert_movies(self, movies_list_to_insert: [dict]) -> [int]:
        filtered_movie_list = self.get_filtered_list_of_documents_to_insert_to_collection(movies_list_to_insert, self.db.movie)
        self.logger.info(f"Inserting movies to DB!")
        inserted_ids = MongoHandler.insert_documents_to_collection(filtered_movie_list, self.db.movie)
        if not inserted_ids:
            raise RuntimeError("Failed to insert movies to DB")
        if len(inserted_ids) < len(filtered_movie_list):
            self.logger.info(f"Failed to insert all documents to DB, {len(inserted_ids)}/{len(filtered_movie_list)}")
        return inserted_ids

    def delete_movies(self, movie_ids_to_delete: [int]):
        deleted_count = MongoHandler.delete_documents_from_collection(movie_ids_to_delete, self.db.movie)
        if deleted_count < len(movie_ids_to_delete):
            raise RuntimeError(f"Failed to remove all movies from db, deleted {deleted_count}/{len(movie_ids_to_delete)}")
        self.logger.info(f"Deleted Movie IDs: {movie_ids_to_delete} from DB!")



