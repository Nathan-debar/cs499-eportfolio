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
            client.server_info()  # Force connection test
            print(f"Connected to database: {db_name}")
            return client
        except errors.ServerSelectionTimeoutError as err:
            raise RuntimeError(f"Could not connect to MongoDB: {err}")

    def _is_valid_dict(self, value: Any) -> bool:
        """Return True if the provided value is a non-empty dictionary."""
        return isinstance(value, dict) and bool(value)

    def _is_valid_number(self, value: Any) -> bool:
        """Return True if the provided value is a non-negative number."""
        return isinstance(value, (int, float)) and value >= 0

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

    def search_animals(
        self,
        breed: str = "",
        sex: str = "",
        min_age_weeks: int = None,
        max_age_weeks: int = None,
        outcome_type: str = "",
        sort_field: str = "breed",
        sort_direction: int = 1,
    ) -> list:
        """
        Search for animals using multiple optional filters.

        Returns:
            list: Matching records, or an empty list if invalid or unsuccessful.
        """
        # Validate numeric search inputs before building the query
        if min_age_weeks is not None and not self._is_valid_number(min_age_weeks):
            return []

        if max_age_weeks is not None and not self._is_valid_number(max_age_weeks):
            return []

        query = {}

        # Add exact-match filters only when provided
        if breed:
            query["breed"] = breed

        if sex:
            query["sex_upon_outcome"] = sex

        if outcome_type:
            query["outcome_type"] = outcome_type

        # Build age-range query if either bound is provided
        if min_age_weeks is not None or max_age_weeks is not None:
            age_query = {}
            if min_age_weeks is not None:
                age_query["$gte"] = min_age_weeks
            if max_age_weeks is not None:
                age_query["$lte"] = max_age_weeks
            query["age_upon_outcome_in_weeks"] = age_query

        try:
            cursor = self.collection.find(
                query,
                {
                    "_id": 0,  # Exclude MongoDB internal id from results
                    "animal_id": 1,
                    "name": 1,
                    "breed": 1,
                    "sex_upon_outcome": 1,
                    "age_upon_outcome_in_weeks": 1,
                    "outcome_type": 1,
                },
            ).sort(sort_field, sort_direction)

            return list(cursor)
        except errors.PyMongoError:
            return []

    def get_distinct_values(self, field_name: str) -> list:
        """
        Return sorted distinct values for a given field.

        Returns:
            list: Distinct values, or an empty list if invalid or unsuccessful.
        """
        if not isinstance(field_name, str) or not field_name.strip():
            return []

        try:
            return sorted(self.collection.distinct(field_name))
        except errors.PyMongoError:
            return []

    def close(self) -> None:
        """Close the MongoDB client connection."""
        if self.client:
            self.client.close()