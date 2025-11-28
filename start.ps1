# Quick Start Script for Lost and Found System
# Run this after initial setup

Write-Host "Lost & Found System - Quick Start" -ForegroundColor Green
Write-Host "==================================`n"

# Check if virtual environment exists
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Run migrations
Write-Host "`nApplying database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Check for superuser
Write-Host "`n" -ForegroundColor Yellow
$createSuperuser = Read-Host "Do you want to create a superuser? (y/n)"
if ($createSuperuser -eq 'y') {
    python manage.py createsuperuser
}

# Create sample categories
Write-Host "`n" -ForegroundColor Yellow
$createCategories = Read-Host "Do you want to create sample item categories? (y/n)"
if ($createCategories -eq 'y') {
    python manage.py shell -c "
from lostfound.models import ItemCategory
ItemCategory.objects.get_or_create(name='Electronics', defaults={'description': 'Phones, laptops, tablets, etc.'})
ItemCategory.objects.get_or_create(name='Documents', defaults={'description': 'IDs, certificates, papers, etc.'})
ItemCategory.objects.get_or_create(name='Accessories', defaults={'description': 'Bags, wallets, keys, jewelry, etc.'})
ItemCategory.objects.get_or_create(name='Clothing', defaults={'description': 'Jackets, shoes, hats, etc.'})
ItemCategory.objects.get_or_create(name='Books', defaults={'description': 'Textbooks, notebooks, etc.'})
print('Sample categories created successfully!')
"
}

Write-Host "`n==================================`n" -ForegroundColor Green
Write-Host "Setup complete! Starting development server..." -ForegroundColor Green
Write-Host "Access the application at: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Django Admin at: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server.`n" -ForegroundColor Yellow

python manage.py runserver
