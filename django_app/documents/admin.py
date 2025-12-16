from django.contrib import admin
from .models import Document, AuditLog


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'approver', 'status', 'created_at')
    list_filter = ('status', 'approver')
    search_fields = ('title', 'description')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'user', 'action', 'timestamp')
    list_filter = ('action', 'user')
    search_fields = ('document__title', 'comment')