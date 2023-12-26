from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Provider, CustomUser, Seeker
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import Group
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .serializer import ProviderSerializer, UserSerializer, SeekerSerializer, LoginSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from scholar_ships.permissions import isProvider, isSeeker

# #Email
# from django.contrib.sites.shortcuts import get_current_site  
# from django.utils.encoding import force_bytes
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
# from django.template.loader import render_to_string  
# from .tokens import account_activation_token  
# from django.contrib.auth.models import User  
# from django.core.mail import EmailMessage  
# from django.contrib.auth import get_user_model
# from django.http import HttpResponse







@api_view(['POST'])
@permission_classes([AllowAny]) 
@csrf_exempt
def register(request):
    if request.method == 'POST':
        
        if 'work_email' in request.data and 'ed_level' in request.data:
            return Response({"Message": "Unvalid information provided "}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'work_email' in request.data:
                
            seri = ProviderSerializer(data=request.data)
        
            if seri.is_valid():
                
                e=seri.save()
                if 'Error Message'in e: 
                    return Response({"Message":e }, status=status.HTTP_200_OK)
                
                return Response({"Message": "Provider Created Successfully"}, status= status.HTTP_201_CREATED)
            else:
                return Response({"Message": "Error in validating data"}, status= status.HTTP_400_BAD_REQUEST)
        
        elif 'ed_level' in request.data:
            seri = SeekerSerializer(data=request.data)
        
            if seri.is_valid():
                e=seri.save()
                if 'Error Message'in e: 
                    return Response({"Message":e }, status=status.HTTP_200_OK)
                
                return Response({"Message": "Seeker Created Successfully"}, status= status.HTTP_201_CREATED)
            else:
                return Response({"Message": "Error in validating data"}, status= status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"Message": "Problem with the provided information"}, status= status.HTTP_400_BAD_REQUEST)
        
        
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
# Token consists of Header: Containst metadata, Payload: contains the claims or information, you can include here user specific data, Signature: Ensures the Integrity of the token 

# Access Token Payload:
# {'token_type': 'access', 'exp': 1701552668, 'iat': 1701549068, 'jti': 'f78728eeef294e55a640b7c7855634e8', 'user_id': 24, 'email': 'Alii@gmail.com', 'role': 'provider', 'iss': 'BATATA-SUPER'}

def is_token_expired(token):
    try:
        # Attempt to decode the token
        decoded_token = AccessToken(token)
        # Check the token's expiration claim
        return decoded_token.is_expired
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
                return Response({'token': token})

        return Response({'error': 'No token found'}, status=status.HTTP_400_BAD_REQUEST)



def testing_token(token,):
    refresh = RefreshToken(token['refresh'])
    access = AccessToken(token['access'])

    print("Access Token Payload:")
    print(access.payload)  # Access token payload data

    print("Refresh Token Payload:")
    print(refresh.payload)  # Refresh token payload data



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_exempt
def login_provider(request):
    
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_provider:
            provider = CustomUser.objects.get(email=email, is_provider=True)
            provider_id = provider.id            
            try:
                refresh = RefreshToken.for_user(user)

                # Customize the payload with user information
                refresh['email'] = email
                refresh['role']  = "provider"       # Add other necessary user information to the payload
                refresh['iss']   = 'BATATA-SUPER'
                refresh['id']    = provider_id
                
                
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response({"Message":"Provider Login Successfuly","Token":token}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"Message": "Error at generating token"}, status= status.HTTP_400_BAD_REQUEST)

        else:
            # User authentication failed or not a provider
            return Response({"Message": "Invalid email, password, or not a provider"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"Message": "UUUU Enter correct email and password"}, status=status.HTTP_400_BAD_REQUEST)
        
        


    

@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_exempt
def login_seeker(request):
    print(request.data)
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_seeker:
            seeker = CustomUser.objects.get(email=email, is_seeker=True)
            seeker_id = seeker.id          
            try:
                refresh = RefreshToken.for_user(user)

                # Customize the payload with user information
                refresh['email'] = email
                refresh['role']  = "seeker"       # Add other necessary user information to the payload
                refresh['iss']   = 'BATATA-SUPER'
                refresh['id']    = seeker_id
                
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(token, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"Message": "Error at generating token"}, status= status.HTTP_400_BAD_REQUEST)

        else:
            # User authentication failed or not a provider
            return Response({"Message": "Invalid email, password, or not a seeker"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"Message": "Enter correct email and password"}, status=status.HTTP_400_BAD_REQUEST)
        
        



@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def view_provider(request):
    
    providers = CustomUser.objects.filter(is_provider = True)
    seri = UserSerializer(providers,many=True)
    return Response(seri.data)



    
    
