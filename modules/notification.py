from notifypy import Notify


def send_notification(title: str, content: str) -> None:
	"""
	Creates a notification.
	:param title: The title of the notification
	:param content: The contents of the notification
	"""
	notification = Notify()
	notification.title = title
	notification.message = content
	notification.send()
