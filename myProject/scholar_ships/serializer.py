from rest_framework import serializers
from .models import Scholarship
from user.models import CustomUser
from .models import Scholarship_Seeker




class ScholarshipSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)  # 'use_url=True' to get image URL in response

    class Meta:
        model = Scholarship
        exclude = ('created_at', 'status', 'id', 'seeker')  
        
    def get_image_url(self, obj):
        if obj.images:
            return self.context['request'].build_absolute_uri(obj.images.url)
        return None
            


class ViewCustomUserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(read_only=True)
    # first_name = serializers.CharField(read_only=True)
    # last_name = serializers.CharField(read_only=True)
    
    def to_representation(self, value):
        # Retrieve the provider object
        try:
            provider = CustomUser.objects.get(pk=value)
        except CustomUser.DoesNotExist:
            return "Error In finding the CustomUser"
        # Access and return the desired field
        return {
            'email': provider.email,
            'first_name' : provider.first_name,
            'last_name' : provider.last_name
            }
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name'
        ]


class ViewScholarshipSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(use_url=True)  # 'use_url=True' to get image URL in response
    # Since you haven't identify the name of the id django creates a id with this nameing convention regarding of inheritance modelName_id, only and only if you don't define it yourself 
    provider = ViewCustomUserSerializer(source='provider_id',read_only=True)  # By setting the source attribute of the nested serializer to 'provider_id', you're explicitly telling the serializer to look for this specific field (the provider_id) within the scholarship object and use its value to retrieve the corresponding CustomUser data. 

    class Meta:
        model = Scholarship
        fields = [
            'category',
            'name',
            'image',
            'description',
            'end_date',
            'start_date',
            'scholar_link',
            'provider',
        ]
        
    def get_image_url(self, obj):
        if obj.images:
            return self.context['request'].build_absolute_uri(obj.images.url)
        return None
    
    



class  ViewScholarshipSeekerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  Scholarship_Seeker
        
        fields = '__all__'
        
        
    