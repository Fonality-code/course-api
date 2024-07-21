
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from config.config import Settings
from beanie import init_beanie


# models 
from models.courses import Course
from models.content import Content
from models.enrollment import Enrollment
from models.payment import Payment

documents = [
    Content,
    Course,
    Enrollment,
    Payment
]




async def init_db():
    # Create a new client and connect to the server
    client = AsyncIOMotorClient(Settings().MONGODB_URL, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    database = client[Settings().DATABASE_NAME]
    try:
        await init_beanie(database=database, document_models=documents)
        client.admin.command('ping')
        print("You successfully connected to Database!")
    except Exception as e:
        print(e)
        print("Database Not Connected!")

