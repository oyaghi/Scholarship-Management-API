from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializer import ProviderSerializer, UserSerializer, SeekerSerializer, LoginSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

# #Email
from django.core.mail import send_mail
from django.conf import settings
from .tokens import EmailVerificationTokenGenerator
from django.utils.http import urlsafe_base64_encode  # For encoding the user ID
from django.utils.encoding import force_bytes  # For ensuring consistent byte representation
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode




# Start of Email thing 

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def re_send_email_verification(request):
    user = request.data
    try:
        # Creating Verification Email
        user             = CustomUser.objects.get(email=user['email'])
        token_generator  = EmailVerificationTokenGenerator()
        token            = token_generator.make_token(user)
        uidb64           = urlsafe_base64_encode(force_bytes(user.pk))
        current_site     = get_current_site(request)
        verification_url = f"https://{current_site.domain}/user/activate/{uidb64}/{token}/"
        
        # Sending the email 
        subject         = 'Email verification'
        message         = f'Hi {user.first_name}\nPlease Verify Your Email\n{verification_url}'
        email_from      = settings.EMAIL_HOST_USER
        recipient_list  = [user.email,]
        send_mail(subject, message,email_from,recipient_list)
        return Response({"Message": f"The Verification Email has been sent again Please check your email"}, status= status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"Message": str(e)})



def EmailVerification(request,user):
    try:
        # Creating Verification Email
        user             = CustomUser.objects.get(email=user['email'])
        token_generator  = EmailVerificationTokenGenerator()
        token            = token_generator.make_token(user)
        uidb64           = urlsafe_base64_encode(force_bytes(user.pk))
        current_site     = get_current_site(request)
        verification_url = f"https://{current_site.domain}/user/activate/{uidb64}/{token}/"
        
        # Sending the email 
        subject         = 'Email verification'
        message         = f'Hi {user.first_name}\nPlease Verify Your Email\n{verification_url}'
        email_from      = settings.EMAIL_HOST_USER
        recipient_list  = [user.email,]
        send_mail(subject, message,email_from,recipient_list)
        return "Email has been sent successfully"
    except Exception as e:
        return str(e)


# End of Email thing 



def activate(request, uidb64, token):  
    
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = CustomUser.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and EmailVerificationTokenGenerator().check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!') 




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
                
                user=seri.save()
                if 'Error Message'in user: 
                    return Response({"Message":user }, status=status.HTTP_200_OK)
                
                else:
                    message = EmailVerification(request,user)
                    return Response({"Message":message}, status=status.HTTP_200_OK)

            else:
                return Response({"Message": "Error in validating data"}, status= status.HTTP_400_BAD_REQUEST)
        
        elif 'ed_level' in request.data:
            seri = SeekerSerializer(data=request.data)
        
            if seri.is_valid():
                user=seri.save()
                if 'Error Message'in user: 
                    return Response({"Message":user }, status=status.HTTP_200_OK)
                
                else:
                    message = EmailVerification(request,user)
                    return Response({"Message":message}, status=status.HTTP_200_OK)
            else:
                return Response({"Message": "Error in validating data"}, status= status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"Message": "Problem with the provided information"}, status= status.HTTP_400_BAD_REQUEST)






@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_exempt
def login_provider(request):
    
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_provider and user.is_active:
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
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_seeker and user.is_active:
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




@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def reset_password(request):
    email = request.data.get('email')
    
    try:
        user = CustomUser.objects.get(email=email)
        
        
    except CustomUser.DoesNotExist:
        return Response({"Message": "User does not exist"})
    