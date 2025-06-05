from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from loguru import logger

from k_backend.core.config import settings
from k_backend.core.db import alembic_upgrade
from k_backend.routers import routers, tags
from k_backend.util import KustomJSONResponse, custom_generate_unique_id

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The All-in-One Financial Island",
    version="0.9.0",
    debug=settings.ENVIRONMENT == "local",
    default_response_class=KustomJSONResponse,
    openapi_tags=tags,
    contact={"name": "Tomy Hsieh", "url": "https://github.com/tomy0000000"},
    license_info={
        "name": "MIT",
        "url": "https://github.com/tomy0000000/K-Backend/blob/main/LICENSE",
    },
    generate_unique_id_function=custom_generate_unique_id,
)
logger.info(f"Applicaiton created in {settings.ENVIRONMENT} environment")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto migrate the database on startup
if not app.debug:
    app.add_event_handler("startup", alembic_upgrade)

# Add all routers to the application
for router in routers:
    app.include_router(router)


# Redirect root path to Swagger UI
@app.get("/", include_in_schema=False, tags=["root"])
async def redirect_to_swagger() -> RedirectResponse:
    return RedirectResponse("docs")
