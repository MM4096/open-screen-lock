from modules.file_manager import get_log_file


def clear_log() -> None:
	with open(get_log_file(), "w") as file:
		file.write("")


def add_to_log(message: str, sender: str = "") -> None:
	with open(get_log_file(), "a") as file:
		if sender != "":
			message = f"[{sender}] {message}"
		file.write(message + "\n")