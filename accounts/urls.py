from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, dashboard_router, user_dashboard, admin_dashboard

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_router, name='dashboard_router'),
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
]
