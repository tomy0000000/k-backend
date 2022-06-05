from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .db import alembic_upgrade
from .routers import routers, tags

app = FastAPI(
    title="K",
    description="The All-in-One Financial Island",
    # version=, TODO: get version from pyproject.toml
    contact={"name": "Tomy Hsieh", "url": "https://github.com/tomy0000000"},
    license_info={
        "name": "MIT",
        "url": "https://github.com/tomy0000000/K-Backend/blob/main/LICENSE",
    },
    openapi_tags=tags,
)

for router in routers:
    app.include_router(router)

@app.on_event("startup")
def on_startup():
    alembic_upgrade()


@app.get("/", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse("docs")
