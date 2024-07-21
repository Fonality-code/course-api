from config.config import Settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI
from fastapi import FastAPI

from models.errors import ErrorResponse


from database.mongod import init_db


from routes.v1 import content, course, enrollment, payment


app = FastAPI(
    title=Settings().APP_NAME,
    version=Settings().APP_VERSION,
    description=Settings().APP_DESCRIPTION,
)


# add routers
app.include_router(course.router)
app.include_router(content.router)
app.include_router(enrollment.router)
app.include_router(payment.router)

app = VersionedFastAPI(
    app, enable_latest=True, version_format="{major}", prefix_format="/v{major}"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.exception_handler(Exception)
async def validation_exception_handler(request, exc: Exception):
    return ErrorResponse(
        status_code=500, message="Internal Server Error", errors=str(exc)
    )


async def startup():
    print("Starting up")
    await init_db()


app.add_event_handler("startup", startup)


@app.get("/healthcheck")
def api_healthcheck():
    return "OK 200 - app running successfully"


# # register routers
# app.include_router(course.router)
