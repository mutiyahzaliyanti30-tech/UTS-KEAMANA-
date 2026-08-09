from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_redirect, name="dashboard"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("dashboard/staff/", views.dashboard_staff, name="dashboard_staff"),
    path("dashboard/user/", views.dashboard_user, name="dashboard_user"),
    path("access-denied/", views.access_denied, name="access_denied"),
]
