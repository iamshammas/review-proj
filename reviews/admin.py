from django.contrib import admin
from .models import Advisor, Reviewer, Intern, Lesson, Review

@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    list_display = ['name', 'stack']
    search_fields = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['date', 'intern', 'lesson', 'assigned_reviewer', 'status']
    list_filter = ['date', 'status', 'assigned_reviewer', 'intern__advisor']
    search_fields = ['intern__name', 'lesson__name']
    list_editable = ['status']

admin.site.register(Advisor)
admin.site.register(Intern)
admin.site.register(Lesson)