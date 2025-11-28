from django.urls import path
from .views import (
    item_list, item_detail, report_lost_item, report_found_item,
    my_lost_items, my_found_items, admin_item_list, admin_pending_items,
    admin_item_detail, admin_update_item_status
)

urlpatterns = [
    path('items/', item_list, name='item_list'),
    path('items/report/lost/', report_lost_item, name='report_lost_item'),
    path('items/report/found/', report_found_item, name='report_found_item'),
    path('items/my/lost/', my_lost_items, name='my_lost_items'),
    path('items/my/found/', my_found_items, name='my_found_items'),
    path('items/<str:item_code>/', item_detail, name='item_detail'),
    # staff item management
    path('staff/items/', admin_item_list, name='admin_item_list'),
    path('staff/items/pending/', admin_pending_items, name='admin_pending_items'),
    path('staff/items/<str:item_code>/', admin_item_detail, name='admin_item_detail'),
    path('staff/items/<str:item_code>/update-status/', admin_update_item_status, name='admin_update_item_status'),
]
