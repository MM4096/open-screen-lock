import time

from modules import app_timer
from modules.app_timer import load_app_limits_file, load_usage_file
from modules.notification import send_notification

notified: dict = {
	"300": [],
	"1800": [],
}


def main():
	while True:
		time.sleep(5)
		load_app_limits_file()
		load_usage_file()

		for i in app_timer.app_usages:
			time_left = app_timer.get_time_left(i.app_name)
			if time_left > 1800 and i.app_name in notified["1800"]:
				notified["1800"].remove(i.app_name)
				notified["300"].remove(i.app_name)
			if time_left < 1800 and i.app_name not in notified["1800"]:
				notified["1800"].append(i.app_name)
				send_notification("Time Limit", f"30 minutes are left for {i.app_name}")
			elif time_left < 300 and i.app_name not in notified["300"]:
				notified["300"].append(i.app_name)
				send_notification("Time Limit", f"5 minutes are left for {i.app_name}")

if __name__ == "__main__":
	main()