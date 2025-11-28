from django.db import models
from django.utils import timezone
from accounts.models import User
from lostfound.models import Item

class Claim(models.Model):
    TYPE_OWNER = 'OWNER_CLAIM'
    TYPE_WRONG = 'WRONG_CLAIM'
    TYPE_CHOICES = [
        (TYPE_OWNER, 'Owner Claim'),
        (TYPE_WRONG, 'Wrong Claim'),
    ]
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    claim_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    claim_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_OWNER)
    description = models.TextField()
    proof_text = models.TextField(blank=True, null=True)
    proof_file = models.FileField(upload_to='claims/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_claims')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim {self.claim_id} for {self.item.item_code}"
