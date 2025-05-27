"""
This script manages the settings of the application.
"""
import os

from modules.app_timer import get_app_limits_as_display_string
import modules.app_timer as app_timer
from modules.constants import HELP_TEXT, EDIT_LIMITS_HELP_TEXT
from modules.custom_print import print_error, print_ok, print_warning
from modules.file_manager import create_needed_dirs, is_super_user
from modules.input_typing import float_input, boolean_input
from modules.process import get_processes
from modules.table import create_table

def clear():
	os.system("clear")


def edit_app_limits():
	"""
	Screen for editing app limits
	:return:
	"""
	print("Editing app limits... (use `exit` to go back)")
	while True:
		print("Enter a command (use `help` for a list of commands)")
		command = input().split(" ")
		if command[0] == "help":
			print(EDIT_LIMITS_HELP_TEXT)
		elif command[0] == "exit":
			clear()
			return
		elif command[0] == "list":
			if len(command) < 2:
				print_error("list: missing required argument 'type' (can be: limit, processes)")
				continue
			if command[1] == "limit":
				print(get_app_limits_as_display_string())
			elif command[1] == "processes":
				filter_str: str = ""
				if len(command) > 2:
					filter_str = command[2]
				data: list[list] = [["PID", "Name"]]
				data.extend([list(i) for i in get_processes(filter_str)])
				print(create_table(data, [10, 20]))
		elif command[0] == "add":
			if not is_super_user():
				print_error("add: you need to be root to add an app limit")
				continue

			name = input("Enter the name of the app to limit (can be a portion of)\n")
			limit = float_input("Enter the limit for this app (in seconds)\n")
			use_strict = boolean_input(
				"Should the app name be strict?\n(If set to `true`, only EXACT matches will be considered)\n")
			app_timer.app_limits.append(app_timer.Limit(
				name,
				limit,
				use_strict,
			))
			app_timer.write_limits_to_file()
			print("Limit added successfully!")
		elif command[0] == "del":
			if not is_super_user():
				print_error("del: you need to be root to delete an app limit")
				continue

			if len(command) < 2:
				print_error("del: missing argument 2: `index`")
				continue
			try:
				if int(command[1]) < 0 or int(command[1]) >= len(app_timer.app_limits):
					print(f"del: index [{command[1]}] out of range.")
					continue
				deleted: app_timer.Limit = app_timer.app_limits.pop(int(command[1]))
				app_timer.write_limits_to_file()
				print(f"Limit with index {0} ({deleted.app_name}) deleted.")
			except ValueError:
				print_error(f"del: index wasn't of type [int]")
				continue
		elif command[0] == "edit":
			if not is_super_user():
				print_error("edit: you need to be root to edit an app limit")
				continue

			if len(command) < 2:
				print_error("edit: missing argument 2: `index`")
				continue
			try:
				if int(command[1]) < 0 or int(command[1]) >= len(app_timer.app_limits):
					print_error(f"edit: index [{command[1]}] out of range.")
					continue
				current_item: app_timer.Limit = app_timer.app_limits[int(command[1])]
				name = input(f"Enter the name of the app to limit (can be a portion of)\nCurrent value: {current_item.app_name}\n")
				limit = float_input(f"Enter the limit for this app (in seconds)\nCurrent value: {current_item.timer}\n")
				use_strict = boolean_input(
					f"Should the app name be strict?\n(If set to `true`, only EXACT matches will be considered)\nCurrent value: {current_item.strict_limit}\n")
				app_timer.app_limits[int(command[1])] = app_timer.Limit(
					name,
					limit,
					use_strict,
				)
				app_timer.write_limits_to_file()
				print("Limit updated successfully!")
			except ValueError:
				print_error(f"edit: index wasn't of type [int]")
				continue


		else:
			print_error(f"Not a valid command: [{command[0]}]. Use 'help' to get a list of all commands")



def main_screen():
	"""
	The main screen
	:return:
	"""
	while True:
		print("Enter a command... (or `help` for a list of commands)")
		command = input()
		command = command.split(" ")
		if command[0] == "help":
			print(HELP_TEXT)
		elif command[0] == "exit":
			return
		elif command[0] == "edit":
			if len(command) == 1:
				print_error("edit: missing required argument 2: 'something' (can be: limit)")
				continue
			if command[1] == "limit":
				clear()
				edit_app_limits()
		elif command[0] == "get":
			if len(command) == 1:
				print_error("get: missing required argument 2: 'something' (can be: remaining)")
				continue
			if command[1] == "remaining":
				print(app_timer.get_app_time_remaining_as_display_string())
		elif command[0] == "extra":
			if len(command) < 3:
				if len(command) < 2:
					print_error("extra: missing required argument 2: 'application'")
				print_error("extra: missing required argument 3: 'extra_time'")
				continue
			try:
				float(command[2])
			except ValueError:
				print_error("extra: Argument 2 (extra_time) must be a float")
				continue
			try:
				this_usage = app_timer.get_usage_with_name(command[1])
				if this_usage is None:
					print_error(f"Application [{command[1]}] not found")
					continue
				this_usage.time_used -= float(command[2])
				app_timer.write_usage_to_file()
				print(this_usage.time_used)
				if float(command[2]) > 0:
					print_ok(f"[{command[1]}] was given {float(command[2])} extra seconds")
				else:
					print_warning(f"[{command[1]}] had {abs(float(command[2]))} seconds removed")
			except ValueError:
				print_error(f"Application [{command[1]}] not found")
				continue


		else:
			print_error(f"Not a valid command: [{command[0]}]. Use 'help' to get a list of all commands")


if __name__ == "__main__":
	create_needed_dirs()
	app_timer.load_app_limits_file()
	app_timer.load_usage_file()
	try:
		main_screen()
	except KeyboardInterrupt:
		print("\nExit signal received.")
		exit(0)
