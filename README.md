# Lost and Found System

A centralized digital platform for reporting, tracking, and recovering misplaced items within an institution or community.

## Features

- **User Dashboard**: View lost items, found items, claims, and notifications
- **Item Reporting**: Report lost or found items with detailed information
- **Auto-Generated Tracking IDs**: Each item gets a unique code (e.g., LF-20251128-0001)
- **Claims System**: Users can claim found items with proof
- **Admin Verification**: Staff can review and approve/reject claims
- **Search & Filter**: Browse items by category, type, status, color, date range
- **Notifications**: Users receive updates when items are matched, claimed, or returned
- **Role-Based Access**: Different dashboards for Students, Staff, and Admins

## Tech Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: SQLite (development)
- **Python**: 3.14

## Setup

```powershell
# Navigate to project
cd c:\Users\Admin\Desktop\lost_found_portal

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create sample categories (optional)
python manage.py shell
```

In the Django shell:
```python
from lostfound.models import ItemCategory
ItemCategory.objects.create(name='Electronics', description='Phones, laptops, etc.')
ItemCategory.objects.create(name='Documents', description='IDs, certificates, etc.')
ItemCategory.objects.create(name='Accessories', description='Bags, wallets, keys, etc.')
ItemCategory.objects.create(name='Clothing', description='Jackets, shoes, etc.')
exit()
```

Run the server:
```powershell
python manage.py runserver
```

Access at http://127.0.0.1:8000/

## User Roles

- **STUDENT**: Can report lost/found items, create claims
- **STAFF**: Same as student + basic admin features
- **ADMIN**: Can review claims, manage items, update statuses
- **SUPERADMIN**: Full system access

## URL Structure

### Public/User URLs
- `/` - Home page with search
- `/login/` - User login
- `/register/` - User registration
- `/items/` - Browse all items with filters
- `/items/<item_code>/` - Item details
- `/items/report/lost/` - Report a lost item
- `/items/report/found/` - Report a found item
- `/items/my/lost/` - My lost item reports
- `/items/my/found/` - My found item reports
- `/items/<item_code>/claim/` - Create a claim
- `/claims/my/` - My claims
- `/notifications/` - View notifications
- `/dashboard/` - User dashboard

### Staff/Admin URLs (use `/staff/` prefix)
- `/dashboard/admin/` - Admin dashboard with stats
- `/staff/items/` - Manage all items
- `/staff/items/pending/` - View pending/open items
- `/staff/items/<item_code>/` - Item management
- `/staff/items/<item_code>/update-status/` - Update item status
- `/staff/claims/` - Manage all claims
- `/staff/claims/pending/` - Review pending claims
- `/staff/claims/<claim_id>/` - Claim review (approve/reject)

## Testing

```powershell
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test lostfound.tests
```

## Project Structure

```
lost_found_portal/
├── accounts/          # User management, authentication, roles
├── lostfound/         # Items, categories, reporting
├── claims/            # Claims system, verification
├── notifications/     # Notification system
├── templates/         # HTML templates (Bootstrap 5)
├── static/            # CSS, JS, images
├── media/             # Uploaded files
├── lostfound_portal/  # Project settings
├── manage.py
└── requirements.txt
```

## Models Overview

- **User**: Custom user with roles (STUDENT, STAFF, ADMIN, SUPERADMIN)
- **ItemCategory**: Categories for organizing items
- **Item**: Lost/found items with tracking codes
- **Claim**: Ownership claims with verification workflow
- **Notification**: User notifications for events

## Item Status Flow

OPEN → MATCHED → UNDER_VERIFICATION → RETURNED/CLOSED or REJECTED

## Claim Workflow

1. User submits claim (PENDING)
2. Admin reviews with proof
3. Admin approves/rejects
4. Item status updated
5. Notification sent to claimant
