from DB.connect import MongoDBConnectionManager, MongoDBCollection

# Define database and collection names
DATABASE_NAME = "sample_analytics"
COLLECTION_NAME = "customers"

# Initialize MongoDB connection
connection_manager = MongoDBConnectionManager(database_name=DATABASE_NAME)

try:
    # Connect to MongoDB
    connection_manager.connect()

    # Access the collection
    collection = MongoDBCollection(connection_manager.db, COLLECTION_NAME)

    # --- CREATE ---
    new_document = {"name": "Alice", "age": 28, "email": "alice@example.com"}
    inserted_id = collection.insert_document(new_document)
    print(f"Document inserted with _id: {inserted_id}")

    # --- READ ---
    print("\n--- All Documents ---")
    documents = collection.find_documents()
    for doc in documents:
        print(doc)

    # --- UPDATE ---
    filter_query = {"name": "Alice"}
    update_query = {"$set": {"age": 29}}
    update_result = collection.update_document(filter_query, update_query)
    print(f"\nMatched {update_result['matched_count']} and modified {update_result['modified_count']} document(s).")

    # --- DELETE ---
    delete_query = {"name": "Alice"}
    deleted_count = collection.delete_document(delete_query)
    print(f"\nDeleted {deleted_count} document(s).")

except Exception as e:
    print("Error during MongoDB operations:", e)

finally:
    # Disconnect from MongoDB
    connection_manager.disconnect()
