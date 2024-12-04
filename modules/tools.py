"""
Helper script with useful functions
"""
from math import floor
from typing import Dict


def resize_string(input_str: str, resize_length: int, cut_overflow: bool = True, overflow_symbol: str = "...") -> str:
	"""
	Resizes a string to a given length, by adding spaces to the end of the string
	:param input_str: The string to resize
	:param resize_length: The new length of the string
	:param cut_overflow: Whether to cut long strings or not
	:param overflow_symbol: If `cut_overflow` is `true`, this is the symbol used on cut strings
	:return:
	"""
	if len(input_str) > resize_length:
		if not cut_overflow:
			return input_str
		else:
			# get the required number of characters
			save_amount: int = resize_length - len(overflow_symbol)
			cut_str: str = input_str[:save_amount]
			return cut_str + overflow_symbol

	while len(input_str) < resize_length:
		input_str += " "
	return input_str


def time_to_h_m_s(time: float) -> dict[str, int | float]:
	"""
	Converts a time (float) into a dictionary with keys "hour", "minute" and "second"
	:param time: The time to convert (in seconds)
	:return: A dictionary, with "hour: int", "minute: int", "second: float"
	"""
	hours: int = floor(time / 3600)
	left: float = time % 3600
	minutes: int = floor(left / 60)
	seconds = left - minutes * 60
	return {
		"hour": hours,
		"minute": minutes,
		"second": seconds,
	}

def time_to_short_str(time: float) -> str:
	"""
	Converts a float (as a time) into the format xh:xm:xs
	:param time: The time to convert
	:return: Formatted time, as xh:xm:xs
	"""
	result_arr: list[str] = []
	result = time_to_h_m_s(time)
	hour = result["hour"]
	minute = result["minute"]
	rounded_seconds: float = round(result["second"], 1)
	if result["hour"] != 0:
		result_arr.append(f"{hour}h")
	elif result["minute"] != 0:
		result_arr.append(f"{minute}m")
	elif result["second"] != 0:
		result_arr.append(f"{rounded_seconds}s")

	if len(result_arr) == 0:
		return "0s"
	else:
		return ":".join(result_arr)
