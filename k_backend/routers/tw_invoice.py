from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..auth import get_client
from ..db import get_session
from ..schemas.tw_invoice import (
    Invoice,
    InvoiceDetail,
    InvoiceUpdated,
    InvoiceWrite,
    InvoiceWriteResponse,
)
from ..util import CustomValidationError

TAG_NAME = "Taiwan E-Invoice"
tag = {
    "name": TAG_NAME,
    "description": "Store replica from MOF E-Invoice platform",
    "externalDocs": {
        "description": "電子發票應用API規格",
        "url": "https://www.einvoice.nat.gov.tw/home/DownLoad"
        "?fileName=1510206773173_0.pdf",
    },
}

invoice_router = APIRouter(
    prefix="/tw-invoice",
    tags=[TAG_NAME],
    dependencies=[Depends(get_client)],
    responses={404: {"description": "Not found"}},
)


@invoice_router.post("", response_model=InvoiceWriteResponse)
def create_or_update_invoice(
    *, session: Session = Depends(get_session), invoices: list[InvoiceWrite]
):
    """
    Create or update invoices

    New invoices will be returned with all details, while existing invoices will be
    returned with only updated details.
    Maximum upload per request is 100 invoices.
    """
    if len(invoices) > 100:
        raise CustomValidationError(
            "Maximum upload per request is 100 invoices", ("body")
        )
    created = []
    updated = []
    for invoice in invoices:
        db_invoice = session.get(Invoice, invoice.number)
        if not db_invoice:
            # Create new invoice
            db_invoice = Invoice.from_orm(invoice)
            session.add(db_invoice)
            session.commit()
            session.refresh(db_invoice)
            created.append(db_invoice)
            session.expunge(db_invoice)
        else:
            # Update existing invoice
            new_invoice_data = invoice.dict(exclude_unset=True)
            modified = {}
            for key in new_invoice_data:
                if getattr(db_invoice, key, None) != new_invoice_data[key]:
                    setattr(db_invoice, key, new_invoice_data[key])
                    modified[key] = new_invoice_data[key]
            if not modified:
                continue
            session.add(db_invoice)
            session.commit()
            modified["number"] = invoice.number
            updated.append(InvoiceUpdated(**modified))
    response = InvoiceWriteResponse(created=created, updated=updated)
    return response


@invoice_router.get("", response_model=list[Invoice])
def read_invoices(*, session: Session = Depends(get_session)):
    invoices = session.exec(select(Invoice)).all()
    return invoices


@invoice_router.patch("", response_model=Invoice)
def update_invoice(*, session: Session = Depends(get_session), invoice: Invoice):
    session.merge(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice


@invoice_router.post("/{number}", response_model=list[InvoiceDetail])
def create_invoice_details(
    *,
    session: Session = Depends(get_session),
    number: str,
    invoice_details: list[InvoiceDetail]
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


@invoice_router.get("/{number}", response_model=list[InvoiceDetail])
def read_invoice_details(*, session: Session = Depends(get_session), number: str):
    details = (
        session.query(InvoiceDetail).where(InvoiceDetail.invoice_number == number).all()
    )
    return details
