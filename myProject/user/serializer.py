from rest_framework import serializers
from .models import Provider, Seeker


class ProviderSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    password = serializers.CharField(source='user.password',write_only=True)
    
    class Meta:
        model = Provider
        
        fields = [
            'email',
            'first_name',
            'last_name',
            'work_email',
            'password',
            
            
        ]
        
class SeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seeker
        
        fields = [
            'email',
            'first_name',
            'last_name',
            'ed_level',
            'password',
            
            
        ]