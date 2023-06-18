def picked_language(func):
	async def wrapper(callback, state):
		await func(callback, state, 'eng')
	return wrapper
