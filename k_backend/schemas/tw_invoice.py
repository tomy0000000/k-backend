from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class InvoiceBase(SQLModel):
    number: Optional[str]
    card_type: Optional[str]
    card_number: Optional[str]
    seller_name: Optional[str]
    status: Optional[str]
    donatable: Optional[bool]
    amount: Optional[str]
    period: Optional[str]
    donate_mark: Optional[int]
    seller_tax_id: Optional[str]
    seller_address: Optional[str]
    buyer_tax_id: Optional[str]
    currency: Optional[str]
    timestamp: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "number": "AB12345678",
                "card_type": "3J0002",
                "card_number": "/AB12+-.",
                "seller_name": "悠旅生活事業股份有限公司台中巿第三十七分公司",
                "status": "已確認",
                "donatable": False,
                "amount": "200",
                "period": "11104",
                "donate_mark": 0,
                "seller_tax_id": "50868202",
                "seller_address": "",
                "buyer_tax_id": "",
                "currency": "",
                "timestamp": "2022-04-24T16:30:44",
            }
        }


class InvoiceBaseWithId(InvoiceBase):
    number: str = Field(primary_key=True, nullable=False)


class InvoiceBaseStrict(InvoiceBaseWithId):
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


class Invoice(InvoiceBaseStrict, table=True):
    __tablename__ = "invoice"
    details: list["InvoiceDetail"] = Relationship(back_populates="invoice")


class InvoiceWrite(InvoiceBase):
    """
    Schema for creating or updating invoices, if invoice is not existed yet, it should
    be fitted with Invoice Schema to create a new invoice.
    """

    pass


class InvoiceRead(InvoiceBaseStrict):
    pass


class InvoiceUpdated(InvoiceBaseWithId):
    pass


class InvoiceWriteResponse(SQLModel):
    created: list[Invoice]
    updated: list[InvoiceUpdated]


#
# InvoiceDetail
#


class InvoiceDetailBase(SQLModel):
    invoice_number: Optional[str]
    row_number: Optional[int] = Field()
    description: Optional[str]
    quantity: Optional[str]
    unit_price: Optional[str]
    amount: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "row_number": "1",
                "description": "冰茶密斯朵V",
                "quantity": "2",
                "unit_price": "95.0000",
                "amount": "190",
            }
        }


class InvoiceDetailBaseWithId(InvoiceDetailBase):
    invoice_number: str = Field(
        primary_key=True, foreign_key="invoice.number", nullable=False
    )
    row_number: int = Field(primary_key=True, nullable=False)


class InvoiceDetailBaseStrict(InvoiceDetailBaseWithId):
    description: str
    quantity: str
    unit_price: str
    amount: str


class InvoiceDetail(InvoiceDetailBaseStrict, table=True):
    __tablename__ = "invoice_detail"
    invoice: "Invoice" = Relationship(back_populates="details")


class InvoiceDetailWrite(InvoiceDetailBase):
    """
    Schema for creating or updating invoice details, if invoice is not existed yet, it
    should be fitted with InvoiceDetail Schema to create a new invoice detail.
    """

    pass


class InvoiceDetailRead(InvoiceDetailBaseStrict):
    pass


class InvoiceDetailUpdated(InvoiceDetailBaseWithId):
    pass


class InvoiceDetailWriteResponse(SQLModel):
    created: list[InvoiceDetailRead]
    updated: list[InvoiceDetailUpdated]


#
# InvoiceCarrier
#


class InvoiceCarrier(SQLModel, table=True):
    __tablename__ = "invoice_carrier"
    id: Optional[int] = Field(primary_key=True, nullable=False)
    type: str
    card_id: str
    name: str
