async def get_all_brands(skip, limit):
	return ['Mazda', 'Toyota',]


async def get_models_by_brand(brand_id ,skip, limit):
	if brand_id == 'Mazda':
		return ['6', 'CX-5', 'CX-4']



async def is_model_picked(model_id, user_id):
	if model_id == 'CX-5':
		return True
	else:
		return False