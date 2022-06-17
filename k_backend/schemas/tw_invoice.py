from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class InvoiceBase(SQLModel):
    number: str
    card_type: Optional[str] = None
    card_number: Optional[str] = None
    seller_name: Optional[str] = None
    status: Optional[str] = None
    donatable: Optional[bool] = None
    amount: Optional[str] = None
    period: Optional[str] = None
    donate_mark: Optional[int] = None
    seller_tax_id: Optional[str] = None
    seller_address: Optional[str] = None
    buyer_tax_id: Optional[str] = None
    currency: Optional[str] = None
    timestamp: Optional[datetime] = None


class Invoice(InvoiceBase, table=True):
    __tablename__ = "invoice"
    number: str = Field(primary_key=True, nullable=False)
    card_type: str
    card_number: str
    seller_name: str
    status: str
    donatable: bool
    amount: str
    period: str
    donate_mark: int
    seller_tax_id: str
    seller_address: Optional[str] = None
    buyer_tax_id: Optional[str] = None
    currency: Optional[str] = None
    timestamp: datetime = Field(nullable=False)
    details: list["InvoiceDetail"] = Relationship(back_populates="invoice")


class InvoiceUpdated(InvoiceBase):
    pass


class InvoiceWrite(InvoiceBase):
    """
    Schema for creating or updating invoices, if invoice is not existed yet, it should
    be fitted with Invoice Schema to create a new invoice.
    """

    pass


class InvoiceWriteResponse(SQLModel):
    created: list[Invoice]
    updated: list[InvoiceUpdated]


class InvoiceDetail(SQLModel, table=True):
    __tablename__ = "invoice_detail"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    row_number: int
    description: str
    quantity: str
    unit_price: str
    amount: str
    invoice_number: str = Field(foreign_key="invoice.number", nullable=False)
    invoice: Invoice = Relationship(back_populates="details")


class InvoiceCarrier(SQLModel, table=True):
    __tablename__ = "invoice_carrier"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    type: str
    card_id: str
    name: str
