from modules.custom_print import PrintColors

HELP_TEXT = (f"{PrintColors.OKGREEN}OpenScreenLock{PrintColors.ENDC}\n\n"
			 "Available Commands:\n"
			 "`help`: list all available commands\n"
			 "`exit`: quits the application\n"
			 "`edit [something]`: edit something\n"
			 "\t- limit: brings up the app limit editing screen\n"
			 "`get [something]`: gets something\n"
			 "\t- remaining: gets the remaining time for each application\n"
			 "`extra [application] [extra_time]`: Gives extra time for an application\n"
			 "\t- `application`: The application to give extra time to\n"
			 "\t- `extra_time`: The amount of extra time (in seconds) to allow. If set to a negative number, "
			 		"time will be removed instead.")

EDIT_LIMITS_HELP_TEXT = (f"{PrintColors.OKGREEN}Edit limits{PrintColors.ENDC}\n\n"
						 "`exit`: exit to the main page\n"
						 "`list [type] [other_args (optional)]`: lists information\n"
						 "\t- `limits`: displays the limits in a table\n"
						 "\t- `processes [filter]`: lists all currently running processes.\n"
						 "\t\t- `filter`: (OPTIONAL) query to filter the results with\n"
						 "`add`: adds a new limit\n"
						 "`del [item]`: deletes the limit with the index of [item]\n"
						 "\t- item: the index of the item to delete\n"
						 "`edit [item]`: edits the limit with an index of [item]\n"
						 "\t- item: the index of the item to edit\n")