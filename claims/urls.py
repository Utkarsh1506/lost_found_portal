from django.urls import path
from .views import create_claim_for_item, my_claims, claim_detail, admin_claims_list, admin_claim_detail, admin_pending_claims

urlpatterns = [
    path('claims/my/', my_claims, name='my_claims'),
    path('claims/my/<int:claim_id>/', claim_detail, name='claim_detail'),
    path('items/<str:item_code>/claim/', create_claim_for_item, name='create_claim_for_item'),
    # staff/admin claim management
    path('staff/claims/', admin_claims_list, name='admin_claims_list'),
    path('staff/claims/pending/', admin_pending_claims, name='admin_pending_claims'),
    path('staff/claims/<int:claim_id>/', admin_claim_detail, name='admin_claim_detail'),
]
