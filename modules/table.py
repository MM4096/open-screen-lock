"""
Creates some beautiful* tables
"""
from modules.tools import resize_string


def create_table(data: list[list[str]], col_sizes: list[int]) -> str:
	"""
	Creates a table
	:param data: The data to display in the table
	:param col_sizes: (OPTIONAL) The sizes of the columns
	:return: The table, as a string
	:except ValueError:
	"""
	def draw_line(characters: int) -> str:
		ret_str: str = ""
		for _ in range(characters):
			ret_str += "-"
		return ret_str

	if len(data) == 0:
		return ""
	# Check whether data is a perfect rectangle
	length: int = len(data[0])
	for row in data:
		if len(row) != length:
			ValueError("Column numbers are not consistent!")

	if len(col_sizes) != length:
		ValueError("Column sizes array does not match the amount of columns!")

	row_size: int = 0
	for i in col_sizes:
		row_size += 2
		row_size += i
	row_size += len(col_sizes) + 1

	final_table: str = ""
	final_table = draw_line(row_size) + "\n"
	for index, row in enumerate(data):
		row_str: str = "|"
		for rindex, cell in enumerate(row):
			row_str += f" {resize_string(str(cell), col_sizes[rindex])} |"
		final_table += f"{row_str}\n{draw_line(row_size)}\n"

	return final_table


