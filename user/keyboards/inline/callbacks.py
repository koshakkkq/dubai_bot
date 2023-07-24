from dataclasses import dataclass


class FalseCallback:
	def filter(self, *args, **kwargs):
		return False


@dataclass
class IterCallback:
	prefix = "iter"
	current_page: int
	action: str # "back" to go to back or "BMW" to select bmw

	def pack(self):
		return f"{self.prefix}:{self.current_page}:{self.action}"

	@staticmethod
	def unpack(string):
		try:
			prefix, current_page, action = string.split(":")
			if prefix != IterCallback.prefix or not current_page.isdigit():
				raise ValueError
			return IterCallback(int(current_page), action)
		except ValueError:
			return FalseCallback()

	def filter(self, current_page=None, action=None):
		if current_page is None:
			current_page = self.current_page
		if action is None:
			action = self.action
		return (self.current_page == current_page) and (self.action == action)