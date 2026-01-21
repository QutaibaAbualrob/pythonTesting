from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User

from .models import Contact, SpamReport, UserProfile
from .serializers import (
    UserRegistrationSerializer, 
    ContactSerializer, 
    SpamReportSerializer
)

# 1. User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to register
    throttle_classes = []  # No rate limiting for registration

    def create(self, request, *args, **kwargs):
        # We override create to return the Token immediately upon registration
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create a token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        # Get the user's phone from UserProfile
        user_profile = UserProfile.objects.get(user=user)
        
        return Response({
            "user": {
                "name": request.data.get('name'),
                "phone": user_profile.phone_number,
                "username": user.username
            },
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# 2. Login View
# Custom login that accepts phone number
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = []  # No rate limiting for login
    
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        
        # Validate input
        if not phone:
            return Response(
                {"error": "Phone number is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find user by phone number
        try:
            user_profile = UserProfile.objects.get(phone_number=phone)
            user = user_profile.user
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


# 3. Phone Number Search View
class SearchView(APIView):
    permission_classes = [permissions.IsAuthenticated] # Only logged-in users can search
    # Uses default UserRateThrottle (5/hour) from settings.py

    def get(self, request, number):
        # Format: /search/<number>
        
        # Try to find the number in our Global Directory (Contact)
        try:
            contact = Contact.objects.get(phone_number=number)
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        except Contact.DoesNotExist:
            # Requirements say: "If number exists... return info". 
            # If not found, we return 404.
            return Response(
                {"detail": "Number not found in global directory."}, 
                status=status.HTTP_404_NOT_FOUND
            )


# 4. Spam Reporting View
class SpamReportView(generics.CreateAPIView):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the reporter to the current user
        serializer.save(reporter=self.request.user)

    def create(self, request, *args, **kwargs):
        # Custom logic to handle "Contact doesn't exist yet"
        # Ideally, the frontend sends a 'contact' ID, but usually they send a 'phone_number' or 'phone'.
        # Let's handle the case where the user sends a phone number instead of an ID.
        
        # Accept both 'phone' and 'phone_number' field names
        phone = request.data.get('phone') or request.data.get('phone_number')
        
        if phone is not None:
            # Validate phone is not empty
            if not phone:
                return Response(
                    {"error": "Phone number cannot be empty."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get or Create the contact entry first
            contact, created = Contact.objects.get_or_create(phone_number=phone)
            
            # Update the request data to point to this contact ID
            # request.data is immutable strictly, so we copy it
            data = request.data.copy()
            data['contact'] = contact.id
            
            # Use the modified data for the serializer
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            # Recalculate spam score after a new report
            # Simple logic: count all reports for this contact
            contact.is_spam = True
            contact.spam_score = contact.reports.count()
            contact.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
        else:
            # Standard behavior if contact ID is sent
            return super().create(request, *args, **kwargs)
