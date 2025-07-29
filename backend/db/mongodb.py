import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Universal import block for local and deployment
try:
    from backend.config import Config
except ImportError:
    from config import Config

config = Config()

# MongoDB client and database
client = None
db = None

# Collections
logs_collection = None
predictions_collection = None
explanations_collection = None

async def connect_to_mongodb():
    """Connect to MongoDB with error handling"""
    global client, db, logs_collection, predictions_collection, explanations_collection
    
    try:
        print(f"Connecting to MongoDB: {config.MONGODB_URI}")
        client = AsyncIOMotorClient(config.MONGODB_URI, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        await client.admin.command('ping')
        print("✓ Successfully connected to MongoDB")
        
        # Set up database and collections
        db = client[config.MONGODB_DB]
        logs_collection = db["logs"]
        predictions_collection = db["predictions"]
        explanations_collection = db["explanations"]
        
        # Create indexes
        await ensure_indexes()
        
        return True
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("⚠️  Continuing without database functionality")
        return False
    except Exception as e:
        print(f"✗ Unexpected error connecting to MongoDB: {e}")
        print("⚠️  Continuing without database functionality")
        return False

async def ensure_indexes():
    """Create necessary indexes for optimal performance"""
    try:
        # Logs collection indexes
        await logs_collection.create_index("timestamp", background=True)
        await logs_collection.create_index("component", background=True)
        await logs_collection.create_index("alarm_type", background=True)
        await logs_collection.create_index([("timestamp", -1)], background=True)
        
        # Predictions collection indexes
        await predictions_collection.create_index("timestamp", background=True)
        await predictions_collection.create_index("component", background=True)
        await predictions_collection.create_index("predicted_at", background=True)
        await predictions_collection.create_index([("predicted_at", -1)], background=True)
        
        # Explanations collection indexes
        await explanations_collection.create_index("timestamp", background=True)
        await explanations_collection.create_index("component", background=True)
        await explanations_collection.create_index("generated_at", background=True)
        await explanations_collection.create_index([("generated_at", -1)], background=True)
        
        print("✓ MongoDB indexes created successfully")
        
    except Exception as e:
        print(f"⚠️  Failed to create indexes: {e}")

async def close_mongodb_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("✓ MongoDB connection closed")

# Helper functions for safe database operations
async def safe_insert_one(collection, document):
    """Safely insert a document into a collection"""
    if collection is None:
        print("⚠️  Database not connected, skipping insert")
        return None
    
    try:
        result = await collection.insert_one(document)
        return result
    except Exception as e:
        print(f"⚠️  Failed to insert document: {e}")
        return None

async def safe_find(collection, filter_dict=None, sort_list=None, limit_count=None):
    """Safely find documents in a collection"""
    if collection is None:
        print("⚠️  Database not connected, returning empty list")
        return []
    
    try:
        cursor = collection.find(filter_dict or {})
        
        if sort_list:
            cursor = cursor.sort(sort_list)
        
        if limit_count:
            cursor = cursor.limit(limit_count)
        
        from bson import ObjectId

        def convert_objectid(obj):
            if isinstance(obj, dict):
                return {k: convert_objectid(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_objectid(i) for i in obj]
            elif isinstance(obj, ObjectId):
                return str(obj)
            else:
                return obj

        docs = await cursor.to_list(length=None)
        return [convert_objectid(doc) for doc in docs]
    except Exception as e:
        print(f"⚠️  Failed to find documents: {e}")
        return [] 