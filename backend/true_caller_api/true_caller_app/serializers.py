from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Contact, SpamReport

# 1. User Registration Serializer
# Handles creating a new User AND their UserProfile (phone number)
class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone_number']

    def create(self, validated_data):
        # Extract phone number from the data
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password')
        
        # Create the standard Django User
        user = User.objects.create_user(
            username=validated_data['username'],
            password=password
        )

        # Create the UserProfile linking the User to the phone number
        UserProfile.objects.create(user=user, phone_number=phone_number)
        
        return user


# 2. Contact Serializer (For Search)
# Displays public info about a number
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['phone_number', 'name', 'is_spam', 'spam_score', 'carrier']


# 3. Spam Report Serializer
# Handles submitting a spam report
class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ['contact', 'category', 'comment']
        read_only_fields = ['reporter'] # Reporter is set automatically from the logged-in user

    def create(self, validated_data):
        # We'll set the reporter in the View, not here, or via context
        # But usually in the View: serializer.save(reporter=self.request.user)
        return super().create(validated_data)