from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..auth import get_client
from ..db import get_session
from ..schemas.psp import PSP, PSPCreate, PSPRead

TAG_NAME = "Payment Service Provider"
tag = {
    "name": TAG_NAME,
    "description": "Create and manage payment service providers",
}

psp_router = APIRouter(
    prefix="/psps",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)


@psp_router.post("", name="Create Payment Service Provider", response_model=PSPRead)
def create(*, session: Session = Depends(get_session), psp: PSPCreate):
    db_psp = PSP.from_orm(psp)
    session.add(db_psp)
    session.commit()
    session.refresh(db_psp)
    return db_psp


@psp_router.get("", name="Read Payment Service Providers", response_model=list[PSPRead])
def reads(*, session: Session = Depends(get_session)):
    psps = session.exec(select(PSP)).all()
    return psps
