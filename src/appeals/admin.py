from django.contrib import admin
from .models import (Appeal, Category)

admin.site.register(Category)

@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'app_status', 'creator', 'assigned_to', 'created_at']
