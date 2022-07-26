from . import account, auth, category, currency, payment, psp, tw_invoice

routers = [
    auth.auth_router,
    account.account_router,
    currency.currency_router,
    category.category_router,
    payment.payment_router,
    psp.psp_router,
    tw_invoice.invoice_router,
]

tags = [
    auth.tag,
    account.tag,
    currency.tag,
    category.tag,
    payment.tag,
    psp.tag,
    tw_invoice.tag,
]
