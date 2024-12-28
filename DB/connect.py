from pymongo import MongoClient
from dotenv import load_dotenv
import os


class MongoDBConnectionManager:
    """
    Handles MongoDB connection using environment variables and X.509 certificate authentication.
    """
    def __init__(self, database_name: str):
        load_dotenv()  # Load environment variables from .env
        self.connection_string = os.getenv("MONGO_URI")
        self.certificate_path = os.getenv("CERTIFICATE_PATH")
        self.database_name = database_name
        self.client = None
        self.db = None

    def connect(self):
        """
        Establishes a connection to the MongoDB server.
        """
        try:
            self.client = MongoClient(
                self.connection_string,
                tls=True,
                tlsCertificateKeyFile=self.certificate_path,
            )
            # Ping the server
            self.client.admin.command("ping")
            print("Successfully connected to MongoDB!")

            # Select the database
            self.db = self.client[self.database_name]
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def disconnect(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB.")


class MongoDBCollection:
    """
    Wrapper class for MongoDB collection operations.
    """
    def __init__(self, db, collection_name: str):
        self.collection = db[collection_name]

    def insert_document(self, document: dict):
        """
        Inserts a single document into the collection.
        """
        result = self.collection.insert_one(document)
        return result.inserted_id

    def find_documents(self, filter_query: dict = None):
        """
        Finds documents in the collection matching the filter query.
        """
        filter_query = filter_query or {}
        return list(self.collection.find(filter_query))

    def update_document(self, filter_query: dict, update_query: dict):
        """
        Updates a single document in the collection.
        """
        result = self.collection.update_one(filter_query, update_query)
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}

    def delete_document(self, filter_query: dict):
        """
        Deletes a single document from the collection.
        """
        result = self.collection.delete_one(filter_query)
        return result.deleted_count
