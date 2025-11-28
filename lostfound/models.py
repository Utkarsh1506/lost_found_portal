from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from accounts.models import User
import datetime

class ItemCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Item(models.Model):
    STATUS_OPEN = 'OPEN'
    STATUS_MATCHED = 'MATCHED'
    STATUS_UNDER_VERIFICATION = 'UNDER_VERIFICATION'
    STATUS_RETURNED = 'RETURNED'
    STATUS_CLOSED = 'CLOSED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_MATCHED, 'Matched'),
        (STATUS_UNDER_VERIFICATION, 'Under Verification'),
        (STATUS_RETURNED, 'Returned'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_REJECTED, 'Rejected'),
    ]
    TYPE_LOST = 'LOST'
    TYPE_FOUND = 'FOUND'
    TYPE_CHOICES = [
        (TYPE_LOST, 'Lost'),
        (TYPE_FOUND, 'Found'),
    ]

    item_code = models.CharField(max_length=30, unique=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(ItemCategory, on_delete=models.SET_NULL, null=True, related_name='items')
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    color = models.CharField(max_length=50)
    brand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    location_lost = models.CharField(max_length=200, blank=True, null=True)
    location_found = models.CharField(max_length=200, blank=True, null=True)
    date_lost = models.DateField(blank=True, null=True)
    date_found = models.DateField(blank=True, null=True)
    # Using FileField instead of ImageField to avoid Pillow dependency in this environment
    photo = models.FileField(upload_to='items/', blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=STATUS_OPEN)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_items')
    handled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_item_code(self):
        today = datetime.date.today().strftime('%Y%m%d')
        count_today = Item.objects.filter(created_at__date=datetime.date.today()).count() + 1
        return f"LF-{today}-{count_today:04d}"

    def save(self, *args, **kwargs):
        if not self.item_code:
            self.item_code = self.generate_item_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_code} - {self.title}"
