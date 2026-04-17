import pymongo
from pymongo import MongoClient, errors
from typing import Any


class AnimalShelter:
    """Provides CRUD functionality for the AAC.animals MongoDB collection."""

    def __init__(
        self,
        username: str = "aacuser",
        password: str = "aacuser",
        host: str = "nv-desktop-services.apporto.com",
        port: int = 30611,
        db_name: str = "AAC",
        collection_name: str = "animals",
    ) -> None:
        """Initialize the MongoDB client, database, and collection."""
        self.client = self._connect(username, password, host, port, db_name)
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

    def _connect(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        db_name: str,
    ) -> MongoClient:
        """Create and return a MongoDB client connection."""
        uri = (
            f"mongodb://{username}:{password}@{host}:{port}/"
            f"{db_name}?authSource=admin"
        )

        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.server_info()  # Forces connection test
            print(f"Connected to database: {db_name}")
            return client
        except errors.ServerSelectionTimeoutError as err:
            raise RuntimeError(f"Could not connect to MongoDB: {err}")

    def _is_valid_dict(self, value: Any) -> bool:
        """Return True if the provided value is a non-empty dictionary."""
        return isinstance(value, dict) and bool(value)

    def create(self, data: dict) -> bool:
        """
        Insert one document into the collection.

        Returns:
            bool: True if the insert succeeds, otherwise False.
        """
        if not self._is_valid_dict(data):
            return False

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except errors.PyMongoError:
            return False

    def read(self, query: dict) -> list:
        """
        Find documents matching the given query.

        Returns:
            list: Matching documents, or an empty list if invalid or unsuccessful.
        """
        if not isinstance(query, dict):
            return []

        try:
            return list(self.collection.find(query))
        except errors.PyMongoError:
            return []

    def update(self, filter_query: dict, update_values: dict) -> int:
        """
        Update all documents matching the filter query.

        Returns:
            int: Number of modified documents.
        """
        if not self._is_valid_dict(filter_query) or not self._is_valid_dict(update_values):
            return 0

        try:
            result = self.collection.update_many(filter_query, {"$set": update_values})
            return result.modified_count
        except errors.PyMongoError:
            return 0

    def delete(self, filter_query: dict) -> int:
        """
        Delete all documents matching the filter query.

        Returns:
            int: Number of deleted documents.
        """
        if not self._is_valid_dict(filter_query):
            return 0

        try:
            result = self.collection.delete_many(filter_query)
            return result.deleted_count
        except errors.PyMongoError:
            return 0

    def close(self) -> None:
        """Close the MongoDB client connection."""
        if self.client:
            self.client.close()