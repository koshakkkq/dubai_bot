class OrderStatus:
    PENDING = 0
    ACTIVE = 1
    DONE = 2
    CANCELED = 3


VERBOSE_ORDER_TYPE = (
    (OrderStatus.PENDING, "Pending."),
    (OrderStatus.ACTIVE, "Active."),
    (OrderStatus.DONE, "Done."),
    (OrderStatus.CANCELED, 'Canceled.')
)