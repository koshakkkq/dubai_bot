from aiogram.dispatcher.filters.state import State, StatesGroup


class AddressStates(StatesGroup):
	ADDRESS_STATE = State()


class ApplicationStates(StatesGroup):
	MAIN_STATE = State() # Заглушка