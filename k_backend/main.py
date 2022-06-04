from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .db import alembic_upgrade
from .routers import routers

app = FastAPI(
    title="K",
    # version=, TODO: get version from pyproject.toml
    description="The All-in-One Financial Island",
    contact={"name": "Tomy Hsieh", "url": "https://github.com/tomy0000000"},
    license_info={
        "name": "MIT",
        "url": "https://github.com/tomy0000000/K-Backend/blob/main/LICENSE",
    },
)

for router in routers:
    app.include_router(router)

@app.on_event("startup")
def on_startup():
    alembic_upgrade()


@app.get("/", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse("docs")
