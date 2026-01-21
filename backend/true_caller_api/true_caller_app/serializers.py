from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Contact, SpamReport

# 1. User Registration Serializer
# Handles creating a new User AND their UserProfile (phone number)
class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=True)
    phone = serializers.CharField(max_length=15, required=True)

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        # Check if phone already exists
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def create(self, validated_data):
        name = validated_data['name']
        phone = validated_data['phone']
        
        # Use a combination of name and phone as username to ensure uniqueness
        base_username = name.lower().replace(' ', '_')
        username = f"{base_username}_{phone[-4:]}"
        
        # Check if username exists and make it unique if needed
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"
            counter += 1
        
        # Create the standard Django User with generated password
        user = User.objects.create_user(
            username=username,
            password=f"auto_{phone}"  # Simple auto-generated password
        )

        # Create the UserProfile linking the User to the phone number
        UserProfile.objects.create(user=user, phone_number=phone)
        
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
        read_only_fields = ['reporter']  # Reporter is set automatically from the logged-in user

    def to_internal_value(self, data):
        # Create a mutable copy of the data to avoid modifying the original
        data = data.copy()
        
        # Normalize category to uppercase if present
        if 'category' in data and isinstance(data['category'], str):
            data['category'] = data['category'].upper()
            
        return super().to_internal_value(data)

    def create(self, validated_data):
        # We'll set the reporter in the View, not here, or via context
        # But usually in the View: serializer.save(reporter=self.request.user)
        return super().create(validated_data)