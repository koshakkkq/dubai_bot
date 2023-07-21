from aiogram.dispatcher.filters.state import State, StatesGroup


class AddressStates(StatesGroup):
	ADDRESS_STATE = State()


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