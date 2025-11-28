from .models import Notification

def notify_user(user, title, message, link=None):
    if user:
        Notification.objects.create(user=user, title=title, message=message, link=link)
