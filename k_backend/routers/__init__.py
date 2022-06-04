from .account import account_router
from .auth import auth_router
from .category import category_router
from .currency import currency_router
from .payment import payment_router
from .tw_invoice import invoice_router

routers = [
    auth_router,
    account_router,
    currency_router,
    invoice_router,
]
