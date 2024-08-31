from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI
from pymongo import MongoClient
from config.config import Settings
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient


# models



documents = []


async def init_db():
    # Create a new client and connect to the server
    client = AsyncIOMotorClient(Settings().MONGODB_URL, server_api=ServerApi("1"))

    # Initialize Beanie with the database and document models
    try:
        await init_beanie(
            database=client[Settings().DATABASE_NAME], document_models=documents
        )

        # Send a ping to confirm a successful connection
        await client.admin.command("ping")
        print("You successfully connected to Database!")
    except Exception as e:
        print(e)
        print("Database Not Connected!")
