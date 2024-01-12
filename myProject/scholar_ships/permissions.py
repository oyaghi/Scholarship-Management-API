from rest_framework.permissions import BasePermission
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import Group
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from datetime import datetime
from rest_framework.exceptions import PermissionDenied






def is_token_expired(token):
    try:
        # Attempt to decode the token
        decoded_token = AccessToken(token)
        # Get the token's expiration time
        token_exp = decoded_token['exp']
        # Get the current time
        current_time = datetime.utcnow().timestamp()
        # Compare token's expiration time with current time
        return token_exp < current_time
    except (TokenError, InvalidToken):
        return True

def get_token(request):
        # Access the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header:
            # Extract the token string from the Authorization header (assuming Bearer token)
            # Format: 'Bearer <token_string>'
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
                
                # Now you have the token string to use for further processing
                return token

        raise PermissionDenied("No token has been provided, provide a Bearer token")


class isProvider(BasePermission):
    
    def has_permission(self, request, view):
        # Authenticate the request using JWTAuthentication
        token = get_token(request)
        if token:
            
            if is_token_expired(token):
                raise PermissionDenied("Token is expired")
            
            access = AccessToken(token)

            
            if  access.payload['role'] =='provider' and access.payload['iss'] == "BATATA-SUPER":
                return True 
            else:
                raise PermissionDenied("This token don't belong to provider ")
            
            

class isSeeker(BasePermission):
    
    def has_permission(self, request, view):  # This method is responsible for checking permissions at the view level.
        # Authenticate the request using JWTAuthentication
        token = get_token(request)
        if token:
            
            if is_token_expired(token):
                raise PermissionDenied("Token is expired")
            
            access = AccessToken(token)

            
            if  access.payload['role'] =='seeker' and access.payload['iss'] == "BATATA-SUPER":
                return True 
            else:
                raise PermissionDenied("This token don't belong to seeker ")
            
            
class isOwner(BasePermission):
    message= "You are not the owner of this Scholarship"
    def has_object_permission (self, request, view, obj):  # This method is used for object-level permissions.
        return obj.provider.user == request.user