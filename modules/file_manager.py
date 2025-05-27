import getpass
import os.path
import stat

import platformdirs
from os.path import join as path_join
from os import makedirs

from modules.custom_print import print_error

def is_super_user() -> bool:
	return os.getuid() == 0

def get_actual_user() -> str:
	return os.environ.get('SUDO_USER') or os.environ.get('LOGNAME') or os.environ.get('USER')

def create_needed_dirs() -> None:
	"""
	Creates all needed directories
	:return:
	"""
	if not os.path.exists(get_user_data_dir()):
		# make sure that root permissions are being used
		if is_super_user():
			makedirs(get_user_data_dir())

			locked_files = [get_config_file_path(), get_app_times_file_path(), get_time_left_file_path(), get_last_refreshed_date_path()]
			for i in locked_files:
				with open(i, "w") as file:
					file.write("")
					# change permissions to root
					os.chown(i, 0, 0)
					# give all users read access
					os.chmod(i, stat.S_IROTH | stat.S_IWUSR | stat.S_IRUSR)

		else:
			print_error("You need to run this script as root at least once!")
			exit(1)


def get_user_data_dir() -> str:
	"""
	:return: The user data directory
	"""
	return path_join("/home", get_actual_user(), ".local/share/OpenScreenLock")


def get_log_file() -> str:
	"""
	:return: The log file path
	"""
	return path_join(get_user_data_dir(), "log.txt")


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