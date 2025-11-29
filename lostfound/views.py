from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, ItemCategory
from .forms import LostItemForm, FoundItemForm
from claims.models import Claim
from django.utils import timezone
from django.contrib import messages

@login_required
def report_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.item_type = 'LOST'
            item.reported_by = request.user
            item.save()
            messages.success(request, f'Lost item reported successfully. Tracking code: {item.item_code}.')
            return redirect('item_detail', item_code=item.item_code)
    else:
        form = LostItemForm()
    return render(request, 'lostfound/report_lost.html', {'form': form})

@login_required
def report_found_item(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.item_type = 'FOUND'
            item.reported_by = request.user
            item.save()
            messages.success(request, f'Found item submitted successfully. Tracking code: {item.item_code}.')
            return redirect('item_detail', item_code=item.item_code)
    else:
        form = FoundItemForm()
    return render(request, 'lostfound/report_found.html', {'form': form})

@login_required
def my_lost_items(request):
    items = Item.objects.filter(reported_by=request.user, item_type='LOST').order_by('-created_at')
    return render(request, 'lostfound/my_lost_items.html', {'items': items})

@login_required
def my_found_items(request):
    items = Item.objects.filter(reported_by=request.user, item_type='FOUND').order_by('-created_at')
    return render(request, 'lostfound/my_found_items.html', {'items': items})

def item_list(request):
    items = Item.objects.all().order_by('-created_at')
    category = request.GET.get('category')
    item_type = request.GET.get('item_type')
    status = request.GET.get('status')
    color = request.GET.get('color')
    q = request.GET.get('q')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if category:
        items = items.filter(category__slug=category)
    if item_type:
        items = items.filter(item_type=item_type)
    if status:
        items = items.filter(status=status)
    if color:
        items = items.filter(color__icontains=color)
    if q:
        items = items.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if date_from:
        items = items.filter(created_at__date__gte=date_from)
    if date_to:
        items = items.filter(created_at__date__lte=date_to)
    categories = ItemCategory.objects.filter(is_active=True)
    return render(request, 'lostfound/item_list.html', {
        'items': items,
        'categories': categories,
        'filters': request.GET,
    })

def item_detail(request, item_code):
    item = get_object_or_404(Item, item_code=item_code)
    can_claim = False
    if request.user.is_authenticated and item.item_type == 'FOUND' and item.status == 'OPEN':
        # user must not already have a pending claim
        can_claim = not Claim.objects.filter(item=item, claimant=request.user, status='PENDING').exists()
    return render(request, 'lostfound/item_detail.html', {'item': item, 'can_claim': can_claim})

@login_required
def admin_item_list(request):
    if not request.user.is_admin_role():
        return redirect('user_dashboard')
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'lostfound/admin_item_list.html', {'items': items})

@login_required
def admin_pending_items(request):
    if not request.user.is_admin_role():
        return redirect('user_dashboard')
    items = Item.objects.filter(status='OPEN').order_by('-created_at')
    return render(request, 'lostfound/admin_pending_items.html', {'items': items})

@login_required
def admin_item_detail(request, item_code):
    if not request.user.is_admin_role():
        return redirect('user_dashboard')
    item = get_object_or_404(Item, item_code=item_code)
    return render(request, 'lostfound/admin_item_detail.html', {'item': item})

@login_required
def admin_update_item_status(request, item_code):
    if not request.user.is_admin_role():
        return redirect('user_dashboard')
    item = get_object_or_404(Item, item_code=item_code)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [c[0] for c in Item.STATUS_CHOICES]:
            item.status = new_status
            item.handled_by = request.user
            item.save()
            messages.success(request, f'Item {item.item_code} status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status selected.')
        return redirect('admin_item_detail', item_code=item.item_code)
    return render(request, 'lostfound/admin_item_update_status.html', {'item': item, 'choices': Item.STATUS_CHOICES})
