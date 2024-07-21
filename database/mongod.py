import motor.motor_asyncio
from config.config import Settings
from beanie import init_beanie




documents = [

]



async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(Settings().MONGODB_URL)
    await init_beanie(database=client.db_name, document_models=documents)