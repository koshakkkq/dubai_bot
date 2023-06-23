async def get_available_orders(user_id, skip, limit):
    return ['Mazda CX-5', 'Mazda 6']

async def get_available_order_info(order_id:str):
    return {
        'brand': 'Mazda',
        'model': order_id.split('_')[-1],
        'part': 'wheel',
        'additional': 'I need 2 wheels for my car, for regular use.',
    }


async def get_active_orders(user_id, skip, limit):
    return ['Mazda CX-5', 'Mazda 6']