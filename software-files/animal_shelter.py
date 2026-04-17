import pymongo
from pymongo import MongoClient, errors


class AnimalShelter:
    """Provide create and read functionality for AAC.animals."""

    def __init__(
        self,
        username: str = "aacuser",
        password: str = "aacuser",
        host: str = "nv-desktop-services.apporto.com",
        port: int = 30611,
        db_name: str = "AAC",
        collection_name: str = "animals",
    ):
        """Initialize client, database, and collection handles."""
        uri = (
            f"mongodb://{username}:{password}@{host}:{port}/"
            f"{db_name}?authSource=admin"
        )

        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.database = self.client[db_name]
            self.collection = self.database[collection_name]
            print(f"Connected to {db_name}.{collection_name}")
        except errors.ServerSelectionTimeoutError as err:
            raise RuntimeError(f"Could not connect to MongoDB: {err}")

    # C in CRUD: insert a single document

    def create(self, data: dict) -> bool:
        """
        Insert one document into the collection.
        Return True on success, False on failure or bad input.
        """
        if not isinstance(data, dict) or not data:
            return False
        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except Exception as err:
            # Log or print err in real code
            return False

 
    # R in CRUD: read documents with a query
    
    def read(self, query: dict) -> list:
        """
        Find documents matching `query` and return them as a list.
        If query is not a dict or an error occurs, return [].
        """
        if not isinstance(query, dict):
            return []
        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except Exception as err:
            # Log or print err in real code
            return []
        
    def update(self, filter_query: dict, update_values: dict) -> int:
        """
        Update documents
        """
        if not (isinstance(filter_query, dict) and isinstance(update_values, dict)):
            return 0
        try:
            result = self.collection.update_many(filter_query, {"$set": update_values})
            return result.modified_count
        except Exception:
            return 0

    def delete(self, filter_query: dict) -> int:
        """
        Delete documents 
        """
        if not isinstance(filter_query, dict):
            return 0
        try:
            result = self.collection.delete_many(filter_query)
            return result.deleted_count
        except Exception:
            return 0
        
        