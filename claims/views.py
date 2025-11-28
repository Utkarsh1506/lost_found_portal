from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Claim
from .forms import ClaimForm
from lostfound.models import Item
from notifications.utils import notify_user

@login_required
def create_claim_for_item(request, item_code):
    item = get_object_or_404(Item, item_code=item_code)
    if request.method == 'POST':
        form = ClaimForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()
            notify_user(item.reported_by, 'New Claim Submitted', f'A claim was submitted for item {item.item_code}.', f'/claims/my/{claim.claim_id}/')
            return redirect('claim_detail', claim_id=claim.claim_id)
    else:
        form = ClaimForm()
    return render(request, 'claims/create_claim.html', {'form': form, 'item': item})

@login_required
def my_claims(request):
    claims = Claim.objects.filter(claimant=request.user).order_by('-created_at')
    return render(request, 'claims/my_claims.html', {'claims': claims})

@login_required
def claim_detail(request, claim_id):
    claim = get_object_or_404(Claim, claim_id=claim_id, claimant=request.user)
    return render(request, 'claims/claim_detail.html', {'claim': claim})

@login_required
def admin_claims_list(request):
    if not request.user.is_admin_role():
        return redirect('user_dashboard')
    claims = Claim.objects.all().order_by('-created_at')
    return render(request, 'claims/admin_claims_list.html', {'claims': claims})

@login_required
def admin_pending_claims(request):
    if not request.user.is_admin_role():
        return redirect('user_dashboard')
    claims = Claim.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'claims/admin_pending_claims.html', {'claims': claims})

@login_required
def admin_claim_detail(request, claim_id):
    if not request.user.is_admin_role():
        return redirect('user_dashboard')
    claim = get_object_or_404(Claim, claim_id=claim_id)
    item = claim.item
    if request.method == 'POST' and claim.status == 'PENDING':
        action = request.POST.get('action')
        if action == 'approve':
            claim.status = 'APPROVED'
            claim.reviewed_by = request.user
            claim.reviewed_at = timezone.now()
            item.status = 'RETURNED'
            item.handled_by = request.user
            claim.save(); item.save()
            notify_user(claim.claimant, 'Claim Approved', f'Your claim {claim.claim_id} for item {item.item_code} was approved.', f'/items/{item.item_code}/')
        elif action == 'reject':
            claim.status = 'REJECTED'
            claim.reviewed_by = request.user
            claim.reviewed_at = timezone.now()
            claim.save()
            notify_user(claim.claimant, 'Claim Rejected', f'Your claim {claim.claim_id} for item {item.item_code} was rejected.', f'/claims/my/{claim.claim_id}/')
        return redirect('admin_claim_detail', claim_id=claim.claim_id)
    return render(request, 'claims/admin_claim_detail.html', {'claim': claim, 'item': item})
