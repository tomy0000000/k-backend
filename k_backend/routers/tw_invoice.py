from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select

from ..auth import get_client
from ..db import get_session
from ..schemas.tw_invoice import (
    Invoice,
    InvoiceDetail,
    InvoiceDetailRead,
    InvoiceDetailUpdated,
    InvoiceDetailWrite,
    InvoiceDetailWriteResponse,
    InvoiceRead,
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

    New invoices will be returned with all fields, while existing invoices will be
    returned with only updated fields.
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
            updated.append(InvoiceUpdated.parse_obj(modified))
    response = InvoiceWriteResponse(created=created, updated=updated)
    return response


@invoice_router.get("", response_model=list[InvoiceRead])
def read_invoices(*, session: Session = Depends(get_session)):
    invoices = session.exec(select(Invoice)).all()
    return invoices


@invoice_router.patch("", response_model=InvoiceUpdated)
def update_invoice(*, session: Session = Depends(get_session), invoice: Invoice):
    session.merge(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice


@invoice_router.post("/{number}", response_model=InvoiceDetailWriteResponse)
def create_or_update_invoice_details(
    *,
    session: Session = Depends(get_session),
    number: str = Path(example="AB12345678"),
    invoice_details: list[InvoiceDetailWrite]
):
    """
    Create or update invoice details

    New details will be returned with all fields, while existing details will be
    returned with only updated fields.
    Maximum upload per request is 100 details.
    """
    if len(invoice_details) > 100:
        raise CustomValidationError(
            "Maximum upload per request is 100 details", ("body")
        )
    db_invoice = session.get(Invoice, number)
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    created = []
    updated = []
    for detail in invoice_details:
        db_detail = session.get(
            InvoiceDetail, {"invoice_number": number, "row_number": detail.row_number}
        )
        if not db_detail:
            # Create new detail
            detail.invoice_number = number
            db_detail = InvoiceDetail.from_orm(detail)
            session.add(db_detail)
            session.commit()
            session.refresh(db_detail)
            created.append(db_detail)
            session.expunge(db_detail)
        else:
            # Update existing detail
            new_detail_data = detail.dict(exclude_unset=True)
            modified = {}
            for key in new_detail_data:
                if getattr(db_detail, key, None) != new_detail_data[key]:
                    setattr(db_detail, key, new_detail_data[key])
                    modified[key] = new_detail_data[key]
            if not modified:
                continue
            session.add(db_detail)
            session.commit()
            modified["invoice_number"] = number
            modified["row_number"] = detail.row_number
            updated.append(InvoiceDetailUpdated.parse_obj(modified))
    response = InvoiceDetailWriteResponse(created=created, updated=updated)
    return response


@invoice_router.get("/{number}", response_model=list[InvoiceDetailRead])
def read_invoice_details(*, session: Session = Depends(get_session), number: str):
    details = (
        session.query(InvoiceDetail).where(InvoiceDetail.invoice_number == number).all()
    )
    return details
