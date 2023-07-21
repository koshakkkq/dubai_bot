import shop.logic.shop_info
async def get_shop_info_message(user_id, language='eng'):
	company_information = await shop.logic.shop_info.get_shop_information(user_id)
	if language == 'eng':
		msg = \
			f"Company name: {company_information['name']}\n"\
			f"📍 Location: {company_information['location']}\n" \
			f"📲 Phone: {company_information['phone']}\n\n" \
			f"If you want to choose spare parts for which brands and models you have, click <Brands and models> button."
		return msg