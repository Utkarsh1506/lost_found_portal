from django.contrib import admin
from .models import Claim

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['claim_id', 'item', 'claimant', 'claim_type', 'status', 'created_at']
    list_filter = ['status', 'claim_type', 'created_at']
    search_fields = ['item__item_code', 'claimant__username', 'description']
    readonly_fields = ['claim_id', 'created_at']
