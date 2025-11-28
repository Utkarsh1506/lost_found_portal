from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import RegistrationForm
from .models import User
from lostfound.models import Item
from claims.models import Claim
from notifications.models import Notification


def home_view(request):
    # simple search bar for items
    query = request.GET.get('q')
    items = Item.objects.all().order_by('-created_at')[:12]
    if query:
        items = Item.objects.filter(title__icontains=query)[:50]
    return render(request, 'base_home.html', {'items': items, 'query': query})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard_router(request):
    if request.user.is_admin_role():
        return redirect('admin_dashboard')
    return redirect('user_dashboard')

@login_required
def user_dashboard(request):
    my_lost = Item.objects.filter(reported_by=request.user, item_type='LOST').order_by('-created_at')[:10]
    my_found = Item.objects.filter(reported_by=request.user, item_type='FOUND').order_by('-created_at')[:10]
    my_claims = Claim.objects.filter(claimant=request.user).order_by('-created_at')[:10]
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:10]
    return render(request, 'accounts/user_dashboard.html', {
        'my_lost': my_lost,
        'my_found': my_found,
        'my_claims': my_claims,
        'notifications': notifications,
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role():
        return redirect('user_dashboard')
    total_items = Item.objects.count()
    open_items = Item.objects.filter(status='OPEN').count()
    pending_claims = Claim.objects.filter(status='PENDING').count()
    returned_items = Item.objects.filter(status='RETURNED').count()
    return render(request, 'accounts/admin_dashboard.html', {
        'total_items': total_items,
        'open_items': open_items,
        'pending_claims': pending_claims,
        'returned_items': returned_items,
    })
