from django.urls import path
from .views import notifications_list, notifications_unread, notification_mark_read

urlpatterns = [
    path('notifications/', notifications_list, name='notifications_list'),
    path('notifications/unread/', notifications_unread, name='notifications_unread'),
    path('notifications/<int:pk>/read/', notification_mark_read, name='notification_mark_read'),
]
