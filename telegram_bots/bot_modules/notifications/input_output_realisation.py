from bot_modules.notifications.notifications import Notifications
from bot_modules.notifications.notifications_abstraction import NotificationsAbstraction


notifications = Notifications()
notifications_abs = NotificationsAbstraction(notifications)
