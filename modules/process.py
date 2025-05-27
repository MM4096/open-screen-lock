"""
Python wrapper for `psutil`
"""
import psutil

from modules.custom_print import print_error


def get_processes(filter_str: str = "", use_strict: bool = False) -> list[(str, str)]:
	"""
	Gets all processes running
	:param filter_str: Only return processes whose name contains this string
	:param use_strict: If set to `true`, then only processes that EXACTLY match the given filter will be returned (case-insensitive)
	:return:
	"""
	ret_arr: list[(str, str)] = []
	for process in psutil.process_iter(["pid", "name"]):
		try:
			if (
					filter_str == "" or
					(not use_strict and filter_str.lower() in process.info["name"].lower()) or
					# Don't need to check for `use_strict`.
					(use_strict and filter_str.lower() == process.info["name"].lower())
			):
				ret_arr.append((process.info["pid"], process.info["name"]))
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return ret_arr


def kill_process(pid: str) -> None:
	"""
	Kills a process
	:param pid: The process to kill
	:return:
	"""
	try:
		proc = psutil.Process(int(pid))
		proc.terminate()
	except Exception as e:
		print_error(str(e))
