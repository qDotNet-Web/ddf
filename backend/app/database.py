from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

db: AsyncIOMotorDatabase = None

def get_database() -> AsyncIOMotorDatabase:
    return db

async def connect_to_mongo():
    global db
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client['ddf_db']


async def close_mongo_connection():
    db.client.close()
