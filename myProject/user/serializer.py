from rest_framework import serializers
from .models import Provider, Seeker, CustomUser
from django.contrib.auth.models import Group
from django.db import transaction,IntegrityError




class ProviderSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(write_only=True)   # Write only for fields that shouldn't be represented and just wants to used for update or create 
    first_name = serializers.CharField(write_only=True)  # We have used write_only = True on all the fields that are being inheirted since we sys can't find them in the Provider model, and we want to tell him that we just want to use them for create or update 
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    work_email = serializers.EmailField()  # Added for Provider's work_email field
        
    class Meta:
        model = Provider
        
        fields = [
            'email',
            'first_name',
            'last_name',
            'work_email',
            'password',
            
        ]
        
        
    def create(self, validated_data):
        user_data = {
            'email': validated_data['email'].lower(),
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'password': validated_data['password'],
            'is_provider':True
        }

        with transaction.atomic():
            try:
    
                user = CustomUser.objects.create_user(**user_data)
                
                provider = Provider.objects.create(
                    user=user,
                    work_email=validated_data['work_email'].lower()
                )
                serializer = ProviderSerializer(provider) # when you try to serialize the object for the response, it is still in an unsaved state and therefore cannot be converted to JSON correctly.
                data = serializer.data
                group = Group.objects.get(name='Provider')

                    # Add the user to the group
                group.user_set.add(user)
                
                return user_data
            except IntegrityError as e:
                
                return ({"Error Message": str(e)})
        
        
            



class SeekerSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)   # Write only for fields that shouldn't be represented and just wants to used for update or create 
    first_name = serializers.CharField(write_only=True)  # We have used write_only = True on all the fields that are being inheirted since we sys can't find them in the Provider model, and we want to tell him that we just want to use them for create or update 
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    ed_level = serializers.CharField()  # Added for Provider's work_email field
        

    class Meta:
        model = Seeker
        
        fields = [
            'email',
            'first_name',
            'last_name',
            'ed_level',
            'password',
            
            
        ]
        
    
    def create(self, validated_data):
        user_data = {
            'email': validated_data['email'].lower(),
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'password': validated_data['password'],
            'is_seeker':True
        }
        with transaction.atomic():
            try:
    
                user = CustomUser.objects.create_user(**user_data)
                
                seeker = Seeker.objects.create(
                    user=user,
                    ed_level=validated_data['ed_level']
                )
                serializer = SeekerSerializer(seeker) # when you try to serialize the object for the response, it is still in an unsaved state and therefore cannot be converted to JSON correctly.
                data = serializer.data
                group = Group.objects.get(name='Seeker')

                    # Add the user to the group
                group.user_set.add(user)

                return user_data
            except IntegrityError as e:
                return ({"Error Message": str(e)})
        
        
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]
        
        
class User2Serializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ['email', 'first_name', 'last_name', 'work_email']
        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = CustomUser
        
        fields = ['email','password']
        
        
        
