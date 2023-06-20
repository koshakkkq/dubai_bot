def picked_language(func):
	async def wrapper(*args, **kwargs):#todo а как это можено написать нормально,сделать массив с разрешёнными kwargs?
		if "command" in kwargs:
			del kwargs['command']
		if "raw_state" in kwargs:
			del kwargs['raw_state']
		kwargs['language'] = 'eng'
		await func(*args, **kwargs)
	return wrapper
