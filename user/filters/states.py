from aiogram.dispatcher.filters.state import State, StatesGroup


class ApplicationStates(StatesGroup):
	MAIN_STATE = State() # Заглушка


class CarDetailStates(StatesGroup):
	BRAND_STATE = State()
	MODEL_STATE = State()
	YEAR_STATE = State()
	DETAIL_TYPE_STATE = State()
	DETAIL_NAME_STATE = State()
	ARTICLE_STATE = State()


class LanguageStates(StatesGroup):
	MAIN_STATE = State()


class ResponseStates(StatesGroup):
	PRICE_STATE = State()
	ADDRESS_STATE = State()
	PHONE_STATE = State()
	STRIPE_STATE = State()

class OrderState(StatesGroup):
	MAIN_STATE = State()