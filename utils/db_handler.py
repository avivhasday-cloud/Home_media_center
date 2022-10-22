import logging
from itertools import islice
from typing import Union, List

import pymongo

from assets.episode import Episode
from assets.movie import Movie
from assets.series import Series
from assets.subtitles import Subtitles


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

    @staticmethod
    def get_filtered_docs_from_collection(collection: pymongo.collection.Collection,  list_of_ids: [str] = None, list_of_names: [str] = None, sort_by: Union[dict, int] = 1, limit: int = 1000):
        if list_of_ids is not None:
            documents = MongoHandler.query_documents_from_collection(MongoFields.ID_KEY_FIELD, list_of_ids, collection, sort_by, limit)
        elif list_of_names is not None:
            documents = MongoHandler.query_documents_from_collection("name", list_of_names, collection, sort_by, limit)
        else:
            documents = MongoHandler.query_documents_from_collection(MongoFields.ID_KEY_FIELD, MongoFields.ALL_EXISTS_DOCS, collection, sort_by, limit)
        return documents

    @staticmethod
    def get_object_list_from_docs(_object: any, documents: [dict]) -> [any]:
        return [_object(**doc) for doc in documents]

    def get_filtered_list_of_documents_to_insert_to_collection(self, documents_list: [dict], collection: pymongo.collection.Collection) -> [dict]:
        documents_names_in_db = [doc["name"] for doc in documents_list if MongoHandler.is_document_already_exists("name", doc["name"], collection)]
        self.logger.info(f"There are {len(documents_names_in_db)}/{len(documents_list)} documents that already exists in DB, Filtering documents list to insert!")
        filtered_docs = list(filter(lambda x: x["name"] not in documents_names_in_db, documents_list))
        return filtered_docs

    def get_movies(self, list_of_ids: [str] = None, list_of_names: [str] = None, sort_by: Union[dict, int] = 1, limit: int = 1000) -> [Movie]:
        documents = MongoHandler.get_filtered_docs_from_collection(self.db.movie, list_of_ids, list_of_names, sort_by, limit)
        return MongoHandler.get_object_list_from_docs(Movie, documents)

    def update_movie(self, movie_id: str, new_movie_details: dict):
        res = MongoHandler.update_document_in_collection(movie_id, new_movie_details, self.db.movie)
        if not res:
            raise RuntimeError(f"Failed to update movie {movie_id}")
        self.logger.info(f"Updated Movie: {movie_id} successfully in DB!")

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
        #todo: delete related data
        deleted_count = MongoHandler.delete_documents_from_collection(movie_ids_to_delete, self.db.movie)
        if deleted_count < len(movie_ids_to_delete):
            raise RuntimeError(f"Failed to remove all movies from db, deleted {deleted_count}/{len(movie_ids_to_delete)} inserted!")
        self.logger.info(f"Deleted Movie IDs: {movie_ids_to_delete} from DB!")

    def get_series(self, list_of_ids: [str] = None, list_of_names: [str] = None, sort_by: Union[dict, int] = 1, limit: int = 1000) -> [Series]:
        documents = MongoHandler.get_filtered_docs_from_collection(self.db.series, list_of_ids, list_of_names, sort_by, limit)
        return MongoHandler.get_object_list_from_docs(Series, documents)

    def update_series(self, series_id: str, series_new_details: [dict]):
        res = MongoHandler.update_document_in_collection(series_id, series_new_details, self.db.series)
        if not res:
            raise RuntimeError(f"Failed to update series {series_id}")
        self.logger.info(f"Updated Series: {series_id} successfully in DB!")

    def insert_series(self, series_list_to_insert: [dict]):
        filtered_series_list = self.get_filtered_list_of_documents_to_insert_to_collection(series_list_to_insert, self.db.series)
        self.logger.info(f"Inserting series to DB!")
        inserted_ids = MongoHandler.insert_documents_to_collection(filtered_series_list, self.db.series)
        if not inserted_ids:
            raise RuntimeError("Failed to insert series to DB")
        if len(inserted_ids) < len(filtered_series_list):
            self.logger.info(f"Failed to insert all documents to DB, {len(inserted_ids)}/{len(filtered_series_list)} inserted!")
        return inserted_ids

    def delete_series(self, series_id_to_delete: [int]):
        #todo: remove data related to documents
        deleted_count = MongoHandler.delete_documents_from_collection(series_id_to_delete, self.db.series)
        if deleted_count < len(series_id_to_delete):
            raise RuntimeError(f"Failed to remove all series from db, deleted {deleted_count}/{len(series_id_to_delete)} inserted!")
        self.logger.info(f"Deleted series IDs: {series_id_to_delete} from DB!")

    def get_episodes(self, series_id: str = None, list_of_ids: [str] = None, list_of_names: [str] = None, sort_by: Union[dict, int] = 1, limit: int = 1000):
        if series_id is not None:
            documents = MongoHandler.query_documents_from_collection("series_id", series_id, self.db.episode, sort_by, limit)
        else:
            documents = MongoHandler.get_filtered_docs_from_collection(self.db.episode, list_of_ids, list_of_names,
                                                                       sort_by, limit)
        return MongoHandler.get_object_list_from_docs(Episode, documents)

    def update_episode(self, episode_id: str, episode_new_details: [dict]):
        res = MongoHandler.update_document_in_collection(episode_id, episode_new_details, self.db.episode)
        if not res:
            raise RuntimeError(f"Failed to update episode {episode_id}")
        self.logger.info(f"Updated Episode: {episode_id} successfully in DB!")

    def insert_episodes(self, episode_list_to_insert: [dict]):
        filtered_episode_list = self.get_filtered_list_of_documents_to_insert_to_collection(episode_list_to_insert, self.db.episode)
        self.logger.info(f"Inserting episodes to DB!")
        inserted_ids = MongoHandler.insert_documents_to_collection(filtered_episode_list, self.db.episode)
        if not inserted_ids:
            raise RuntimeError("Failed to insert episode to DB")
        if len(inserted_ids) < len(filtered_episode_list):
            self.logger.info(f"Failed to insert all documents to DB, {len(inserted_ids)}/{len(filtered_episode_list)} inserted!")
        return inserted_ids

    def delete_episodes(self, episodes_id_to_delete: [int]):
        deleted_count = MongoHandler.delete_documents_from_collection(episodes_id_to_delete, self.db.episode)
        if deleted_count < len(episodes_id_to_delete):
            raise RuntimeError(f"Failed to remove all episodes from db, deleted {deleted_count}/{len(episodes_id_to_delete)} inserted!")
        self.logger.info(f"Deleted episodes IDs: {episodes_id_to_delete} from DB!")

    def get_subtitles(self, list_of_ids: [str] = None, asset_id: str = None, sort_by: Union[dict, int] = 1, limit: int = 1000) -> [Subtitles]:
        if asset_id is not None:
            documents = MongoHandler.query_documents_from_collection("asset_id", asset_id, self.db.subtitles, sort_by, limit)
        else:
            documents = MongoHandler.get_filtered_docs_from_collection(self.db.subtitles, list_of_ids, None, sort_by, limit)

        return MongoHandler.get_object_list_from_docs(Subtitles, documents)

    def update_subtitles(self, subtitles_id: str, subtitles_new_details: [dict]):
        res = MongoHandler.update_document_in_collection(subtitles_id, subtitles_new_details, self.db.subtitles)
        if not res:
            raise RuntimeError(f"Failed to update subtitles {subtitles_id}")
        self.logger.info(f"Updated Subtitles: {subtitles_id} successfully in DB!")

    def insert_episodes(self, subtitles_list_to_insert: [dict]):
        filtered_subtitles_list = self.get_filtered_list_of_documents_to_insert_to_collection(subtitles_list_to_insert, self.db.subtitles)
        self.logger.info(f"Inserting subtitles to DB!")
        inserted_ids = MongoHandler.insert_documents_to_collection(filtered_subtitles_list, self.db.subtitles)
        if not inserted_ids:
            raise RuntimeError("Failed to insert subtitles to DB")
        if len(inserted_ids) < len(filtered_subtitles_list):
            self.logger.info(f"Failed to insert all documents to DB, {len(inserted_ids)}/{len(filtered_subtitles_list)} inserted!")
        return inserted_ids

    def delete_episodes(self, subtitles_id_to_delete: [int]):
        deleted_count = MongoHandler.delete_documents_from_collection(subtitles_id_to_delete, self.db.subtitles)
        if deleted_count < len(subtitles_id_to_delete):
            raise RuntimeError(f"Failed to remove all subtitles from db, deleted {deleted_count}/{len(subtitles_id_to_delete)} inserted!")
        self.logger.info(f"Deleted subtitles IDs: {subtitles_id_to_delete} from DB!")
