def float_input(label: str, error_text: str="Input must be a float!") -> float:
	"""
	Creates an input that only accepts float inputs
	:param error_text: The text to display on error
	:param label: The text to display on the input
	:return: The float input returned
	"""
	while True:
		result = input(label)
		try:
			return float(result)
		except ValueError:
			print(error_text)
			continue

def boolean_input(label: str, error_text: str="Input must be one of: \"YyNnTtFf\"") -> bool:
	"""
	Creates an input that only accepts boolean inputs
	:param error_text: The text to display on error
	:param label: The text to display on the input
	:return: The boolean input returned
	"""
	while True:
		result = input(label)
		if result.lower() in ["y", "t"]:
			return True
		elif result.lower() in ["n", "f"]:
			return False
		print(error_text)