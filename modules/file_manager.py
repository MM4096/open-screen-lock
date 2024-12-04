import os.path

import platformdirs
from os.path import join as path_join
from os import makedirs


def create_needed_dirs() -> None:
	"""
	Creates all needed directories
	:return:
	"""
	if not os.path.exists(get_user_data_dir()):
		makedirs(get_user_data_dir())


def get_user_data_dir() -> str:
	"""
	:return: The user data directory
	"""
	return platformdirs.user_data_dir("OpenScreenLock", "mm4096")


def get_log_file() -> str:
	"""
	:return: The log file path
	"""
	path_join(get_user_data_dir(), "log.txt")


def get_config_file_path() -> str:
	"""
	:return: The path to the settings file
	"""
	return path_join(get_user_data_dir(), "config")


def get_app_times_file_path() -> str:
	""""
	:return: The path to the app restrictions file
	"""
	return path_join(get_user_data_dir(), "times")


def get_time_left_file_path() -> str:
	"""
	:return: The path to the countdown file
	"""
	return path_join(get_user_data_dir(), "timer")


def get_last_refreshed_date_path() -> str:
	"""
	:return: The path to the countdown file
	"""
	return path_join(get_user_data_dir(), "last_reset")