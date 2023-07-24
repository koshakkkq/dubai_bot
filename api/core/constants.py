
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


VERBOSE_RAITING_TYPE = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
)