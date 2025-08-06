#!/usr/bin/env python3
"""
Script to set up Cosmos DB database and container for the AI Navigator Profiler
"""

import os
import json
from azure.cosmos import CosmosClient, PartitionKey

def setup_cosmos_db():
    """Set up the Cosmos DB database and container"""
    
    # Get configuration from environment
    cosmos_endpoint = os.environ.get('COSMOS_ENDPOINT')
    cosmos_key = os.environ.get('COSMOS_KEY')
    database_name = os.environ.get('COSMOS_DATABASE_NAME', 'navigator_profiler')
    container_name = os.environ.get('COSMOS_CONTAINER_NAME', 'sessions')
    
    if not cosmos_endpoint or not cosmos_key:
        print("❌ Error: COSMOS_ENDPOINT and COSMOS_KEY must be set in environment")
        return False
    
    try:
        # Create Cosmos DB client
        client = CosmosClient(cosmos_endpoint, cosmos_key)
        
        print(f"🔗 Connected to Cosmos DB at: {cosmos_endpoint}")
        
        # Create database if it doesn't exist
        try:
            database = client.create_database_if_not_exists(database_name)
            print(f"✅ Database '{database_name}' created/verified")
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return False
        
        # Create container if it doesn't exist
        try:
            container = database.create_container_if_not_exists(
                id=container_name,
                partition_key=PartitionKey(path="/id"),
                offer_throughput=400  # Minimum throughput for serverless
            )
            print(f"✅ Container '{container_name}' created/verified")
        except Exception as e:
            print(f"❌ Error creating container: {e}")
            return False
        
        print("\n🎉 Cosmos DB setup completed successfully!")
        print(f"📊 Database: {database_name}")
        print(f"📦 Container: {container_name}")
        print(f"🔑 Partition Key: /id")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up Cosmos DB: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up Cosmos DB for AI Navigator Profiler...")
    
    # Load settings from local.settings.json
    try:
        with open('local.settings.json', 'r') as f:
            settings = json.load(f)
        
        # Set environment variables
        for key, value in settings['Values'].items():
            os.environ[key] = value
        
        print("📋 Loaded configuration from local.settings.json")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not load local.settings.json: {e}")
        print("Please ensure COSMOS_ENDPOINT and COSMOS_KEY are set in environment")
    
    # Set up the database
    success = setup_cosmos_db()
    
    if success:
        print("\n✅ Setup completed! You can now test the function:")
        print("curl -X POST http://localhost:7071/api/assessment")
    else:
        print("\n❌ Setup failed. Please check your Cosmos DB credentials and try again.") 