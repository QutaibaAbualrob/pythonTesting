from django.contrib import admin
from .models import Contact, SpamReport, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'is_spam', 'spam_score', 'carrier')
    list_filter = ('is_spam',)
    search_fields = ('phone_number', 'name')

@admin.register(SpamReport)
class SpamReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'contact', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('contact__phone_number', 'reporter__username')
