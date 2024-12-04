"""
The process that blocks applications when the time runs out
"""
import math
import os.path
import time

from modules.app_timer import load_usage_file, load_app_limits_file, write_usage_to_file
import modules.app_timer as app_timer
from modules.custom_print import print_warning
from modules.file_manager import get_last_refreshed_date_path
from modules.notification import send_notification
from modules.process import get_processes, kill_process

from datetime import datetime

notified: dict = {
	"300": [],
	"1800": [],
}


def main():
	while True:
		# To not block first thread by always running Python
		# also, timing.
		time.sleep(1)

		# see if a reset should occur
		current_day = datetime.now().day
		current_month = datetime.now().month
		current_year = datetime.now().year
		with open(get_last_refreshed_date_path(), "r") as f:
			last_date = float(f.readline())
			last_month = float(f.readline())
			last_year = float(f.readline())
		if current_day > last_date or current_month > last_month or current_year > last_year:
			for i in app_timer.app_usages:
				i.time_used = 0
				write_usage_to_file()
				with open(get_last_refreshed_date_path(), "w") as f:
					f.write(f"{current_day}\n{current_month}\n{current_year}")
			send_notification("Time Limit", "App times reset!")
			notified["1800"] = []
			notified["300"] = []

		load_app_limits_file()
		load_usage_file()
		for i in app_timer.app_usages:
			try:
				this_limit = app_timer.get_limit_with_name(i.app_name)
				if len(get_processes(i.app_name, this_limit.strict_limit)) > 0:
					i.time_used += 1
					if app_timer.get_time_left(i.app_name) < 1800 and i.app_name not in notified["1800"]:
						notified["1800"].append(i.app_name)
						send_notification("Time Limit", f"30 minutes are left for {i.app_name}")
					elif app_timer.get_time_left(i.app_name) < 300 and i.app_name not in notified["300"]:
						notified["300"].append(i.app_name)
						send_notification("Time Limit", f"5 minutes are left for {i.app_name}")

					if app_timer.get_time_left(i.app_name) == 0:
						i.time_used = this_limit.timer

						for process in get_processes(i.app_name, this_limit.strict_limit):
							send_notification("App Blocked", f"{i.app_name} has been blocked.")
							kill_process(process[0])


			except ValueError:
				print_warning(f"Couldn't find a limit with a name of [{i.app_name}]")

		app_timer.write_usage_to_file()


if __name__ == "__main__":
	if not os.path.exists(get_last_refreshed_date_path()):
		with open(get_last_refreshed_date_path(), "w") as file:
			file.write(f"{datetime.now().day}\n{datetime.now().month}\n{datetime.now().year}")
	load_app_limits_file()
	load_usage_file()
	main()