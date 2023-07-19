import aiohttp


async def make_get_request(url):

	async with aiohttp.ClientSession() as session:
		async with session.get(url) as res:
			if res.status != 200:
				raise Exception(await res.text())
			return await res.json()



async def make_post_request(url, data):
	async with aiohttp.ClientSession() as session:
		async with session.post(url,data=data) as res:
			if res.status != 200:
				raise Exception(await res.text())
			return await res.json()

