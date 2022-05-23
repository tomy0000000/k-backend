from datetime import datetime
from typing import List, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel


class Invoice(SQLModel, table=True):
    __tablename__ = "invoice"
    number: str = Field(primary_key=True)
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
    timestamp: datetime
    details: List["InvoiceDetail"] = Relationship(back_populates="invoice")


class InvoiceDetail(SQLModel, table=True):
    __tablename__ = "invoice_detail"
    id: Optional[int] = Field(default=None, primary_key=True)
    row_number: int
    description: str
    quantity: str
    unit_price: str
    amount: str
    invoice_number: Optional[str] = Field(default=None, foreign_key="invoice.number")
    invoice: Optional[Invoice] = Relationship(back_populates="details")


class InvoiceCarrier(SQLModel, table=True):
    __tablename__ = "invoice_carrier"
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    card_id: str
    name: str
