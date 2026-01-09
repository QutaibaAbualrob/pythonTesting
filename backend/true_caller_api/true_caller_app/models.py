from django.db import models
from django.contrib.auth.models import User

# 1. User Profile
# Extends the default User model to store their phone number.
# Using OneToOneField so each User has exactly one Profile.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.phone_number})"


# 2. Global Directory (Contact)
# This represents the "database" of all known numbers.
# It stores the owner's name and the spam status.
class Contact(models.Model):

    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_spam = models.BooleanField(default=False)
    spam_score = models.IntegerField(default=0) # e.g. count of reports
    
    carrier = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.phone_number} - {self.name}"


# 3. Spam Report
# Records a user reporting a specific number as spam.
class SpamReport(models.Model):

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spam_reports')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='reports')
    category = models.CharField(max_length=50, choices=[
        ('SALES', 'Sales/Telemarketing'),
        ('SCAM', 'Scam/Fraud'),
        ('HARASSMENT', 'Harassment'),
        ('OTHER', 'Other'),
    ])
    
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('reporter', 'contact') # Prevent duplicate reports for same number by same user

    def __str__(self):
        return f"{self.reporter.username} reported {self.contact.phone_number}"