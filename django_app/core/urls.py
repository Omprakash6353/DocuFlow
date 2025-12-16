# django_app/core/urls.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from documents import views as documents_views

urlpatterns = [
    path("", lambda request: redirect("login"), name="home"),
    path("admin/", admin.site.urls),

    # Authentication
    path("login/", documents_views.custom_login, name="login"),
    path("logout/", documents_views.custom_logout, name="logout"),

    # Dashboard and documents
    path("dashboard/", documents_views.dashboard, name="dashboard"),
    path("documents/create/", documents_views.create_document, name="create_document"),
    path("documents/<int:document_id>/", documents_views.document_detail, name="document_detail"),
]