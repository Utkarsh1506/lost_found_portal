from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_STUDENT = 'STUDENT'
    ROLE_STAFF = 'STAFF'
    ROLE_ADMIN = 'ADMIN'
    ROLE_SUPERADMIN = 'SUPERADMIN'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_STAFF, 'Staff'),
        (ROLE_ADMIN, 'Admin'),
        (ROLE_SUPERADMIN, 'Super Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def is_admin_role(self):
        return self.role in {self.ROLE_ADMIN, self.ROLE_SUPERADMIN}
