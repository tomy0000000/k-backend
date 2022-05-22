from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from db import alembic_upgrade
from routers import tw_invoice

app = FastAPI(
    title="K",
    description="The All-in-One Financial Island",
    contact={"name": "Tomy Hsieh", "url": "https://github.com/tomy0000000"},
    license_info={"name": "MIT", "url": "https://github.com/tomy0000000"},
    openapi_tags=[tw_invoice.tag],
)
app.include_router(tw_invoice.router)


@app.on_event("startup")
def on_startup():
    alembic_upgrade()


@app.get("/")
async def redirect_to_swagger():
    return RedirectResponse("docs")
