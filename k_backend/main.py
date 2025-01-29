from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .core.config import settings
from .core.db import alembic_upgrade
from .routers import routers, tags
from .util import KustomJSONResponse

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The All-in-One Financial Island",
    version="0.8.1",
    default_response_class=KustomJSONResponse,
    openapi_tags=tags,
    contact={"name": "Tomy Hsieh", "url": "https://github.com/tomy0000000"},
    license_info={
        "name": "MIT",
        "url": "https://github.com/tomy0000000/K-Backend/blob/main/LICENSE",
    },
)

app.add_event_handler("startup", alembic_upgrade)
for router in routers:
    app.include_router(router)


@app.get("/", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse("docs")
