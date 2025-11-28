from django.contrib import admin
from .models import ItemCategory, Item

@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_code', 'title', 'item_type', 'status', 'reported_by', 'created_at']
    list_filter = ['item_type', 'status', 'category', 'created_at']
    search_fields = ['item_code', 'title', 'description']
    readonly_fields = ['item_code', 'created_at', 'updated_at']
