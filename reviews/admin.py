from django.contrib import admin
from .models import Advisor, Reviewer, Review

@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    list_display = ['name', 'stack']
    search_fields = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['date', 'intern_name', 'lesson_name', 'assigned_reviewer', 'status']
    list_filter = ['date', 'status', 'assigned_reviewer', 'created_by']
    search_fields = ['intern_name', 'lesson_name']
    list_editable = ['status']

admin.site.register(Advisor)