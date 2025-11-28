# Lost and Found System

A centralized digital platform for reporting, tracking, and recovering misplaced items within an institution or community space. This system replaces manual registers and informal communication with a structured, data-driven, and user-friendly solution.

## 🎯 Project Overview

The **Lost and Found System** is designed to help users report, track, and recover misplaced items efficiently. It provides a complete workflow from reporting lost/found items to verification and handover through a secure claim process.

### Key Objectives
- Report lost items easily with detailed information
- Submit found items with proper documentation
- Track the status of submissions in real-time
- Verify ownership through a secure workflow
- Automated notifications for status updates
- Admin panel for complete management

## ✨ Features

### User Features
- **User Dashboard**: View lost items, found items, claims, and notifications
- **Item Reporting**: Report lost or found items with detailed information
- **Auto-Generated Tracking IDs**: Each item gets a unique code (e.g., LF-20251128-0001)
- **Claims System**: Users can claim found items with proof upload
- **Search & Filter**: Browse items by category, type, status, color, date range
- **Notifications**: Real-time updates when items are matched, claimed, or returned
- **Photo Upload**: Attach images to item reports

### Admin Features
- **Admin Verification**: Staff can review and approve/reject claims
- **Dashboard Analytics**: View statistics (total items, open items, pending claims, returned items)
- **Item Management**: Update item status and assign handlers
- **Claims Review**: Review proof documents and approve/reject claims
- **User Management**: Manage user roles and permissions

## Tech Stack

- **Backend**: Django 4.2.7 (Python Web Framework)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.2
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Icons**: Font Awesome 6.4.0
- **Python**: 3.8+
- **Additional**: Pillow 10.1.0 (Image processing)

## 👥 User Roles & Access Control

The system supports four different user roles with varying levels of access:

### 1. STUDENT (Regular User)
- Report lost items
- Submit found items
- Create claims for found items
- Track own submissions
- View notifications

### 2. STAFF (Limited Admin)
- All STUDENT features
- Basic admin access

### 3. ADMIN (Full Administrator)
- Review and approve/reject claims
- Update item statuses
- Manage all items and claims
- View dashboard statistics
- Assign handlers to items

### 4. SUPERADMIN
- Full system access
- User management
- Database administration
- System configuration

## 📊 Database Models

### User Model (accounts.User)
```python
- username, email, password (inherited from AbstractUser)
- role: STUDENT, STAFF, ADMIN, SUPERADMIN
- department: CharField (optional)
- phone: CharField (optional)
- is_verified: BooleanField
```

### ItemCategory Model (lostfound.ItemCategory)
```python
- name: CharField (unique)
- slug: SlugField (auto-generated)
- description: TextField (optional)
- is_active: BooleanField
```

### Item Model (lostfound.Item)
```python
- item_code: Auto-generated (LF-YYYYMMDD-XXXX)
- title, category, color, brand
- item_type: LOST or FOUND
- description: TextField
- location_lost/location_found: CharField
- date_lost/date_found: DateField
- photo: FileField (upload)
- status: OPEN, MATCHED, UNDER_VERIFICATION, RETURNED, CLOSED, REJECTED
- reported_by: ForeignKey to User
- handled_by: ForeignKey to User (admin, optional)
- created_at, updated_at: DateTime
```

### Claim Model (claims.Claim)
```python
- claim_id: AutoField
- item: ForeignKey to Item
- claimant: ForeignKey to User
- claim_type: OWNER_CLAIM, WRONG_CLAIM
- description: TextField
- proof_text: TextField (optional)
- proof_file: FileField (optional)
- status: PENDING, APPROVED, REJECTED, CANCELLED
- reviewed_by: ForeignKey to User (admin)
- reviewed_at: DateTime
- created_at: DateTime
```

### Notification Model (notifications.Notification)
```python
- user: ForeignKey to User
- title: CharField
- message: TextField
- link: CharField (internal URL)
- is_read: BooleanField
- created_at: DateTime
```

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
