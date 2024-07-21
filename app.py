from config.config import Settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI
from fastapi import FastAPI

from database.mongod import init_db


app = FastAPI(
    title=Settings().APP_NAME,
    version=Settings().APP_VERSION,
    description=Settings().APP_DESCRIPTION,
)


app = VersionedFastAPI(app, enable_latest=True, version_format='{major}',
    prefix_format='/v{major}')





app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)



async def startup():
    print("Starting up")
    await init_db()


app.add_event_handler("startup", startup)

@app.get('/')
def index():
    return {
        "API": {
            "version": Settings().APP_VERSION,
            "description": Settings().APP_DESCRIPTION
        }
    }


@app.get("/healthcheck")
def api_healthcheck():
    return "OK 200 - app running successfully"


