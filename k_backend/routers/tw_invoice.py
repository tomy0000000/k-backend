from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..auth import get_client
from ..db import get_session
from ..schemas.tw_invoice import Invoice, InvoiceDetail

TAG_NAME = "Taiwan E-Invoice"
tag = {
    "name": TAG_NAME,
    "description": "Store replica from MOF E-Invoice platform",
    "externalDocs": {
        "description": "電子發票應用API規格",
        "url": "https://www.einvoice.nat.gov.tw/home/DownLoad?fileName=1510206773173_0.pdf",
    },
}

invoice_router = APIRouter(
    prefix="/tw-invoice",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)


@invoice_router.post("", response_model=List[Invoice], tags=["Taiwan E-Invoice"])
def create_invoice(*, session: Session = Depends(get_session), invoices: List[Invoice]):
    response = []
    for invoice in invoices:
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        response.append(invoice)
        session.expunge(invoice)
    return response


@invoice_router.get("", tags=["Taiwan E-Invoice"])
def read_invoices(*, session: Session = Depends(get_session)):
    invoices = session.exec(select(Invoice)).all()
    return invoices


@invoice_router.patch("", tags=["Taiwan E-Invoice"])
def update_invoice(*, session: Session = Depends(get_session), invoice: Invoice):
    session.merge(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice


@invoice_router.post("/{number}", tags=["Taiwan E-Invoice"])
def create_invoice_details(
    *,
    session: Session = Depends(get_session),
    number: str,
    invoice_details: List[InvoiceDetail]
):
    response = []
    for detail in invoice_details:
        if detail.invoice_number != number:
            continue
        session.add(detail)
        session.commit()
        session.refresh(detail)
        response.append(detail)
        session.expunge(detail)
    return response


@invoice_router.get("/{number}", tags=["Taiwan E-Invoice"])
def read_invoice_details(*, session: Session = Depends(get_session), number: str):
    details = (
        session.query(InvoiceDetail).where(InvoiceDetail.invoice_number == number).all()
    )
    return details
