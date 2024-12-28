from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
connection_string = os.getenv("MONGO_URI")
certificate_path = os.getenv("CERTIFICATE_PATH")

try:
    # Connect to MongoDB using X.509
    client = MongoClient(
        connection_string,
        tls=True,
        tlsCertificateKeyFile=certificate_path
    )

    # Ping the server to test the connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    # Access the database
    db = client['sample_analytics']
    collection = db['customers']  # Replace with your desired collection name

    # --- CREATE ---
    # Insert a document into the collection
    new_document = {"name": "Alice", "age": 28, "email": "alice@example.com"}
    insert_result = collection.insert_one(new_document)
    print(f"Document inserted with _id: {insert_result.inserted_id}")

    # --- READ ---
    # Find all documents
    print("\n--- All Documents ---")
    documents = collection.find()
    for doc in documents:
        print(doc)

    # --- UPDATE ---
    # Update a document
    filter_query = {"name": "Alice"}
    update_query = {"$set": {"age": 29}}
    update_result = collection.update_one(filter_query, update_query)
    print(f"\nMatched {update_result.matched_count} document(s) and modified {update_result.modified_count} document(s).")

    # --- DELETE ---
    # Delete a document
    delete_query = {"name": "Alice"}
    delete_result = collection.delete_one(delete_query)
    print(f"\nDeleted {delete_result.deleted_count} document(s).")

except Exception as e:
    print("Failed to connect to MongoDB or perform operations:", e)
