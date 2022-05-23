from typing import List

from db import engine
from fastapi import APIRouter
from schemas import tw_invoice
from sqlmodel import Session, select

tag = {
    "name": "Taiwan E-Invoice",
    "description": "Store replica from MOF E-Invoice platform",
    "externalDocs": {
        "description": "電子發票應用API規格",
        "url": "https://www.einvoice.nat.gov.tw/home/DownLoad?fileName=1510206773173_0.pdf",
    },
}

router = APIRouter(
    prefix="/tw-invoice",
    tags=[tag["name"]],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/invoices/", response_model=List[tw_invoice.Invoice], tags=["Taiwan E-Invoice"]
)
def create_invoice(invoices: List[tw_invoice.Invoice]):
    with Session(engine) as session:
        response = []
        for invoice in invoices:
            print(invoice)
            session.add(invoice)
            session.commit()
            session.refresh(invoice)
            response.append(invoice)
            session.expunge(invoice)
        return response


@router.get("/invoices/", tags=["Taiwan E-Invoice"])
def read_invoices():
    with Session(engine) as session:
        invoices = session.exec(select(tw_invoice.Invoice)).all()
        return invoices


@router.patch("/invoices/", tags=["Taiwan E-Invoice"])
def update_invoice(invoice: tw_invoice.Invoice):
    with Session(engine) as session:
        session.merge(invoice)
        session.commit()
        session.refresh(invoice)
        return invoice


@router.post("/invoices/{number}", tags=["Taiwan E-Invoice"])
def create_invoice_details(
    number: str, invoice_details: List[tw_invoice.InvoiceDetail]
):
    with Session(engine) as session:
        response = []
        for detail in invoice_details:
            if detail.invoice_number != number:
                continue
            print(detail)
            session.add(detail)
            session.commit()
            session.refresh(detail)
            response.append(detail)
            session.expunge(detail)
        return response


@router.get("/invoices/{number}", tags=["Taiwan E-Invoice"])
def read_invoice_details(number: str):
    with Session(engine) as session:
        details = (
            session.query(tw_invoice.InvoiceDetail)
            .where(tw_invoice.InvoiceDetail.invoice_number == number)
            .all()
        )
        return details