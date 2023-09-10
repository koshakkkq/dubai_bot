class OrderStatus:
    PENDING = 0
    ACTIVE = 1
    DONE = 2
    CANCELED = 3


VERBOSE_ORDER_TYPE = (
    (OrderStatus.PENDING, "Pending."),
    (OrderStatus.ACTIVE, "Active."),
    (OrderStatus.DONE, "Finished."),
    (OrderStatus.CANCELED, 'Canceled.')
)


VERBOSE_RAITING_TYPE = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


part_types = ('Body Parts', 'Electric', 'Engine and gearbox', 'Chassis and steering', 'Interior', 'Climate', 'Audio and entertainment')