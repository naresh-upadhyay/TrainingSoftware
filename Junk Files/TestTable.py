from bson.objectid import ObjectId
from DB.connect import MongoDBConnectionManager


class TableDataCRUD:
    def __init__(self, db_name, collection_name):
        # Initialize MongoDB connection
        self.client = MongoDBConnectionManager(database_name=db_name) # Adjust the URI if necessary
        self.client.connect()
        self.db = self.client.db
        self.collection = self.db[collection_name]

    def create(self, data):
        """Create a new document in the collection."""
        try:
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            return f"An error occurred: {e}"

    def read(self, query=None):
        """Read documents from the collection based on the query."""
        try:
            if query is None:
                return list(self.collection.find())
            else:
                return list(self.collection.find(query))
        except Exception as e:
            return f"An error occurred: {e}"

    def update(self, record_id, updated_data):
        """Update an existing document by its _id."""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(record_id)}, {"$set": updated_data}
            )
            if result.matched_count > 0:
                return "Document updated successfully."
            else:
                return "No document found with the given ID."
        except Exception as e:
            return f"An error occurred: {e}"

    def delete(self, record_id):
        """Delete a document by its _id."""
        try:
            result = self.collection.delete_one({"_id": ObjectId(record_id)})
            if result.deleted_count > 0:
                return "Document deleted successfully."
            else:
                return "No document found with the given ID."
        except Exception as e:
            return f"An error occurred: {e}"

# Example Usage
if __name__ == "__main__":
    db_name = "sample_analytics1"
    collection_name = "customers1"
    crud = TableDataCRUD(db_name, collection_name)

    # Create a new document
    new_data = {"name": "John Doe", "age": 30, "email": "john.doe@example.com"}
    document_id = crud.create(new_data)
    print(f"Created document with ID: {document_id}")

    # Read all documents
    documents = crud.read()
    print("All documents:", documents)

    # Update a document
    updated_data = {"age": 31}
    update_result = crud.update(document_id, updated_data)
    print(update_result)

    # Delete a document
    delete_result = crud.delete(document_id)
    print(delete_result)


'''
from bson.objectid import ObjectId
from DB.connect import MongoDBConnectionManager


class DataCRUD:
    def __init__(self, db_name, collection_name):
        """Initialize MongoDB connection."""
        self.client = MongoDBConnectionManager(database_name=db_name)
        self.client.connect()
        self.db = self.client.db
        self.collection = self.db[collection_name]

    def create(self, data):
        """Create a new document in the collection."""
        try:
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            return f"An error occurred: {e}"

    def read(self, query=None):
        """Read documents from the collection based on the query."""
        try:
            if query is None:
                return list(self.collection.find())  # Retrieve all documents
            else:
                return list(self.collection.find(query))  # Retrieve documents based on query
        except Exception as e:
            return f"An error occurred: {e}"

    def update(self, query, updated_data):
        """Update documents in the collection based on the query."""
        try:
            result = self.collection.update_many(query, {"$set": updated_data})
            if result.matched_count > 0:
                return f"{result.matched_count} document(s) updated successfully."
            else:
                return "No documents matched the query to update."
        except Exception as e:
            return f"An error occurred: {e}"

    def delete(self, query):
        """Delete documents from the collection based on the query."""
        try:
            result = self.collection.delete_many(query)
            if result.deleted_count > 0:
                return f"{result.deleted_count} document(s) deleted successfully."
            else:
                return "No documents matched the query to delete."
        except Exception as e:
            return f"An error occurred: {e}"


# Example Usage
if __name__ == "__main__":
    db_name = "sample_analytics1"
    collection_name = "customers1"
    crud = DataCRUD(db_name, collection_name)

    # Create a new document
    new_data = {"name": "John Doe", "age": 30, "email": "john.doe@example.com"}
    document_id = crud.create(new_data)
    print(f"Created document with ID: {document_id}")

    # Read all documents
    documents = crud.read()
    print("All documents:", documents)

    # Read documents by query
    query = {"name": "John Doe"}
    documents = crud.read(query)
    print("Documents by name:", documents)

    # Update documents by query
    update_query = {"name": "John Doe"}
    updated_data = {"age": 31}
    update_result = crud.update(update_query, updated_data)
    print(update_result)

    # Delete documents by query
    delete_query = {"name": "John Doe"}
    delete_result = crud.delete(delete_query)
    print(delete_result)


'''