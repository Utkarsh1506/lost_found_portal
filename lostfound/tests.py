from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User
from .models import ItemCategory, Item
from claims.models import Claim

class LostFoundFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass', role='STUDENT')
        self.admin = User.objects.create_user(username='admin', password='pass', role='ADMIN')
        self.cat = ItemCategory.objects.create(name='Electronics')

    def login(self, user):
        self.client.login(username=user.username, password='pass')

    def test_report_lost_item(self):
        self.login(self.user)
        url = reverse('report_lost_item')
        resp = self.client.post(url, {
            'title': 'Lost Phone',
            'category': self.cat.id,
            'color': 'Black',
            'brand': 'BrandX',
            'description': 'A black phone',
            'location_lost': 'Library',
            'date_lost': '2025-11-01'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.item_type, 'LOST')

    def test_report_found_item(self):
        self.login(self.user)
        url = reverse('report_found_item')
        resp = self.client.post(url, {
            'title': 'Found Phone',
            'category': self.cat.id,
            'color': 'Black',
            'brand': 'BrandX',
            'description': 'A found phone',
            'location_found': 'Cafeteria',
            'date_found': '2025-11-02'
        })
        self.assertEqual(resp.status_code, 302)
        item = Item.objects.get(title='Found Phone')
        self.assertEqual(item.item_type, 'FOUND')

    def test_create_claim_and_approve(self):
        # create found item first
        self.login(self.user)
        self.client.post(reverse('report_found_item'), {
            'title': 'Found Wallet', 'category': self.cat.id, 'color': 'Brown', 'brand': '',
            'description': 'Leather wallet', 'location_found': 'Hall', 'date_found': '2025-11-03'
        })
        item = Item.objects.get(title='Found Wallet')
        # create claim by user
        claim_url = reverse('create_claim_for_item', args=[item.item_code])
        resp = self.client.post(claim_url, {
            'claim_type': 'OWNER_CLAIM',
            'description': 'It is mine',
            'proof_text': 'Has my id card'
        })
        self.assertEqual(resp.status_code, 302)
        claim = Claim.objects.get(item=item)
        self.assertEqual(claim.status, 'PENDING')
        # approve by admin
        self.client.logout()
        self.login(self.admin)
        approve_url = reverse('admin_claim_detail', args=[claim.claim_id])
        resp2 = self.client.post(approve_url, {'action': 'approve'})
        self.assertEqual(resp2.status_code, 302)
        claim.refresh_from_db(); item.refresh_from_db()
        self.assertEqual(claim.status, 'APPROVED')
        self.assertEqual(item.status, 'RETURNED')
