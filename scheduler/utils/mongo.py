import os
from pymongo import MongoClient
from django.conf import settings

# Global variable to store the client instance
_mongo_client = None

def get_db_handle():
    global _mongo_client
    
    uri = os.getenv('MONGO_URI')
    
    if _mongo_client is None:
        _mongo_client = MongoClient(uri)

    # Extract db name from URI or use a default
    db_name = uri.split('/')[-1].split('?')[0]
    if not db_name:
        db_name = 'calendar_copilot'
        
    db = _mongo_client[db_name]
    return db, _mongo_client