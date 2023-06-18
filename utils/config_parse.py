import json
def config_parse():
	with open('config.json') as f:
		data = json.load(f)
		return data