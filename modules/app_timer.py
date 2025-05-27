import math
import os

from modules.custom_print import print_error
from modules.file_manager import get_app_times_file_path, get_last_refreshed_date_path, get_time_left_file_path
from modules.logger import add_to_log
from modules.table import create_table
from modules.tools import time_to_short_str

SEPARATOR_ELEMENT: str = "<~separator~>"


class Limit:
	def __init__(self, app_name: str, timer: float, strict_limit: bool):
		self.app_name: str = app_name
		self.timer: float = timer
		self.strict_limit: bool = strict_limit

	def to_string(self) -> str:
		return f"{self.app_name}{SEPARATOR_ELEMENT}{self.timer}{SEPARATOR_ELEMENT}{self.strict_limit}"

	def to_list(self, use_formatted_time: bool = False) -> list:
		return [
			self.app_name,
			time_to_short_str(self.timer) if use_formatted_time else self.timer,
			self.strict_limit,
			]

	@staticmethod
	def from_string(string: str):
		split_str: list[str] = string.split(SEPARATOR_ELEMENT)
		if len(split_str) < 3:
			ValueError(f"Provided string ({string}) has less than 3 parts!")
		elif len(split_str) > 3:
			ValueError(f"Provided string ({string}) has more than 3 parts!")
		return Limit(
			split_str[0],
			float(split_str[1]),
			split_str[2] == True,
		)

	@staticmethod
	def to_list_of_lists(items: list, use_formatted_time: bool = False) -> list[list]:
		ret_list: list = []
		for i in items:
			if isinstance(i, Limit):
				ret_list.append(i.to_list(use_formatted_time))
		return ret_list


class Usage:
	def __init__(self, app_name: str, time_used: float = 0):
		self.app_name: str = app_name
		self.time_used: float = time_used

	def to_string(self) -> str:
		return f"{self.app_name}{SEPARATOR_ELEMENT}{self.time_used}"

	def to_list(self) -> list:
		return [self.app_name, self.time_used]

	@staticmethod
	def from_string(string: str):
		split_str: list[str] = string.split(SEPARATOR_ELEMENT)
		if len(split_str) < 2:
			ValueError(f"Provided string ({string}) has less than 2 parts!")
		elif len(split_str) > 2:
			ValueError(f"Provided string ({string}) has more than 2 parts!")
		return Usage(
			split_str[0],
			float(split_str[1]),
		)


app_limits: list[Limit] = []
app_usages: list[Usage] = []

#region Limits
def load_app_limits_file() -> None:
	"""
	Loads the config file from [file_manager.get_app_times_file_path()]
	:return:
	"""
	global app_limits
	app_limits = []
	if os.path.exists(get_app_times_file_path()):
		with open(get_app_times_file_path(), "r") as file:
			for line in file.readlines():
				try:
					app_limits.append(Limit.from_string(line))
				except ValueError:
					add_to_log(f"Couldn't parse line ({line}) as a Limit")


def get_app_limits_as_string() -> str:
	"""
	:return: All the app limits as a string
	"""
	string = ""
	for i in app_limits:
		string += i.to_string() + "\n"
	return string

def get_app_limits_as_display_string() -> str:
	"""
	:return: The app limits in a nice table
	"""
	col_sizes: list = [0, 20, 10, 10]
	# Get the length (1-digit, 2-digit, etc.) of the app_limits
	col_sizes[0] = max(len(str(len(app_limits))), 2)
	values: list[list] = [["id", "name", "limit", "strict"]]
	for index, row in enumerate(Limit.to_list_of_lists(app_limits, True)):
		if isinstance(row, list):
			row.insert(0, str(index))
		values.append(row)

	return create_table(values, col_sizes)

def get_app_time_remaining_as_display_string() -> str:
	"""
	:return: The app times remaining in a nice table
	"""
	data: list[list[str]] = [["name", "time_remaining"]]
	load_usage_file()
	for i in app_usages:
		this_list = i.to_list()
		this_list[1] = time_to_short_str(get_time_left(i.app_name))
		data.append(this_list)

	return create_table(data, [30, 20])


def write_limits_to_file() -> None:
	"""
	Writes all the app_limits to the file
	:return:
	"""
	with open(get_app_times_file_path(), "w") as file:
		file.write(get_app_limits_as_string())

def get_limit_with_name(app_name: str) -> Limit | None:
	"""
	Returns the limit of an app with the name "app_name"
	:param app_name: The name of the app to search
	:return: The correct Limit
	:except ValueError
	"""
	for i in app_limits:
		if i.app_name == app_name:
			return i
	ValueError(f"Can't find app with name [{app_name}]")
	return None


#endregion

#region Usage
def load_usage_file():
	"""
	Loads the usages from the file
	:return:
	"""
	global app_usages
	app_usages = []
	if not os.path.exists(get_time_left_file_path()):
		with open(get_time_left_file_path(), "w") as file:
			file.write("")
	with open(get_time_left_file_path(), "r") as file:
		for line in file.readlines():
			try:
				app_usages.append(Usage.from_string(line))
			except ValueError as e:
				print_error(f"An error occurred.\n\n{e}")

	# Add apps without processes
	for limit in app_limits:
		found: bool = False
		for usage in app_usages:
			if limit.app_name == usage.app_name:
				found = True
		if not found:
			app_usages.append(Usage(limit.app_name, 0))


def write_usage_to_file():
	"""
	Writes app_usages to its file
	:return:
	"""
	final_str: str = ""
	for i in app_usages:
		final_str += f"{i.to_string()}\n"
	with open(get_time_left_file_path(), "w") as file:
		file.write(final_str)

def get_usage_with_name(app_name: str) -> Usage:
	"""
	Returns the Usage of an app with the name "app_name"
	:param app_name: The name of the app to search
	:return: The correct Usage
	:except ValueError
	"""
	for i in app_usages:
		if i.app_name == app_name:
			return i
	ValueError(f"Can't find app with name [{app_name}]")
#endregion

def get_time_left(name: str) -> float:
	"""
	Returns the remaining time of a certain app limit (in seconds), or 0 if the timer is already expired
	:param name: The name of the app
	:return: The time remaining for that app (in seconds)
	"""
	used_time: float = 0
	for i in app_usages:
		if i.app_name == name:
			used_time = i.time_used

	total_time: float = math.inf
	for i in app_limits:
		if i.app_name == name and i.timer < total_time:
			total_time = i.timer

	if total_time <= used_time:
		return 0
	else:
		return total_time - used_time