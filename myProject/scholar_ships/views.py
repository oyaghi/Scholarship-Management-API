from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  IsAuthenticated
from rest_framework import status
from .serializer import ScholarshipSerializer, ViewScholarshipSerializer, ViewScholarshipSeekerSerializer
from .models import Scholarship
from .permissions import isProvider, isSeeker, isOwner
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import PermissionDenied
from .models import Scholarship_Seeker




# Create your views here.


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






# @api_view(['POST','GET'])
# @csrf_exempt
# def add_view_scholarship(request):
    
#     if request.method == 'POST':
#         if IsAuthenticated().has_permission(request,add_view_scholarship) and isProvider().has_permission(request,add_view_scholarship):
        
#             token = get_token(request)
#             if token:
                
#                 access = AccessToken(token)
#                 provider_id = access.payload['id']
#                 request.data['provider'] = provider_id
                
#                 seri = ScholarshipSerializer(data=request.data)
                
#                 if seri.is_valid():
#                     seri.save()
                    
#                     return Response({"Message":"Scholarship has been created successfully"}, status=status.HTTP_201_CREATED)
                
#                 else:
#                     return Response({"Message":seri.errors}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"Message": "You don't have permission to access this NOT PROVIDER, Provide a provider token"},status= status.HTTP_401_UNAUTHORIZED)
                
#     elif request.method == "GET":
#         scholars = Scholarship.objects.all()
        
#         # token = get_token(request)
#         # access = AccessToken(token)
#         # provider_id = access.payload['id']
#         # request_data = request.query_params.copy()
#         # request_data['provider'] = provider_id
        
#         if scholars.count() > 1:
#             seri = ViewScholarshipSerializer(scholars,many=True,context={'request': request})
            
#         else:
#             seri = ViewScholarshipSerializer(scholars.first(),context={'request': request})

        
#         return Response({"Message":seri.data}, status = status.HTTP_200_OK)
    
    
    
# For Provider dashboard 
# @api_view(["GET"])
# @permission_classes([isProvider,IsAuthenticated])
# @csrf_exempt
# def provider_scholarship(request):    
    
#     scholars = Scholarship.objects.filter(provider_id = request.user.id)
    
#     if scholars.count() ==1 :
#         seri = ViewScholarshipSerializer(scholars.first())
#     else:
#         seri  = ViewScholarshipSerializer(scholars, many=True)
        
    
#     return Response({"Message": seri.data}, status=status.HTTP_200_OK)


# @api_view(["DELETE","PUT"])
# @permission_classes([isProvider,IsAuthenticated])
# @csrf_exempt
# def delete_update_scholarship(request, pk):
    
#     if request.method == "DELETE":
#         try:
#             scholar = Scholarship.objects.get(pk=pk)
#         except Scholarship.DoesNotExist:
#             return Response({"Message": "Scholarship doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
#         scholar.delete()
#         return Response({"Message": "Scholarship deleted"}, status=status.HTTP_200_OK)
        
#     elif request.method == "PUT":
#         try:
#             scholar = Scholarship.objects.get(pk=pk)
#         except Scholarship.DoesNotExist:
#             return Response({"Message": "Scholarship doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
#         seri = ScholarshipSerializer(partial=True ,instance=scholar, data=request.data)
        
#         if seri.is_valid():
#             seri.save()
#             # if 'Error Message'in e: 
#             #     return Response({"Message":e }, status=status.HTTP_200_OK)
                
#             return Response({"Message": "Scholarship Updated Successfuly"}, status= status.HTTP_200_OK)
#         else:
#             return Response({"Message": "Error in validating data"}, status= status.HTTP_400_BAD_REQUEST)
        
            
        
        
# Api Used to Add scholarship that are interested in for Seekers, Also used to view the fav/intererested scholarship for seeker
# @api_view(["GET"])
# @csrf_exempt
# @permission_classes([isSeeker,IsAuthenticated])
# def FavList(request):
#     token = get_token(request)
#     access = AccessToken(token)

#     if request.method =="GET":
        
#         scholars = Scholarship_Seeker.objects.filter(seeker= access.payload['id'])
        
#         serialized_scholars = []
#         for scholar in scholars:
#             scholarship = Scholarship.objects.get(pk = scholar.scholarship.pk)
#             serialized_scholar = ViewScholarshipSerializer(scholarship, context={'request': request}).data
#             serialized_scholars.append(serialized_scholar)
            
            
#         return Response(serialized_scholars)
    
    
    
# @api_view(["POST"])
# @csrf_exempt
# @permission_classes([isSeeker,IsAuthenticated])
# def Add_Fav(request, pk):
#     token = get_token(request)
#     access = AccessToken(token)


#     if request.method == "POST":
#         data = request.data 
#         data["seeker"] = access.payload['id']
#         data["scholarship"] = pk
        
#         seri = ViewScholarshipSeekerSerializer(data = data)
        
        
#         if seri.is_valid():
#             seri.save()
#         else:
#             return Response({"Message":"Invalid data, item haven't been saved"}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"Message":"Scholarship has been added to favorite list "}, status=status.HTTP_202_ACCEPTED)
    
    





#=======================================================================================
#Class Based Views

from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404


@method_decorator(csrf_exempt, name='dispatch')
class AddViewScholarship(APIView):
    
    def post(self,request):
        
        if IsAuthenticated().has_permission(request,self.post) and isProvider().has_permission(request,self.post):
        
            token = get_token(request)
            if token:
                
                access = AccessToken(token)
                provider_id = access.payload['id']
                request.data['provider'] = provider_id
                
                seri = ScholarshipSerializer(data=request.data)
                
                if seri.is_valid():
                    seri.save()
                    
                    return Response({"Message":"Scholarship has been created successfully"}, status=status.HTTP_201_CREATED)
                
                else:
                    return Response({"Message":seri.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Message": "You don't have permission to access this NOT PROVIDER, Provide a provider token"},status= status.HTTP_401_UNAUTHORIZED)
                
    def get(self,request):
        
        scholars = Scholarship.objects.all()
        
        if scholars.count() > 1:
            seri = ViewScholarshipSerializer(scholars,many=True,context={'request': request})
            
        else:
            seri = ViewScholarshipSerializer(scholars.first(),context={'request': request})

        
        return Response({"Message":seri.data}, status = status.HTTP_200_OK)
    


@method_decorator(csrf_exempt, name='dispatch')
class DeleteUpdateScholarships(APIView):
    
    permission_classes = [isProvider, IsAuthenticated, isOwner]

    def delete(self,request, pk):
        
        try:
            scholar = Scholarship.objects.get(pk=pk)
        except Scholarship.DoesNotExist:
            return Response({"Message": "Scholarship doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, scholar)  # Check object-level permission
        scholar.delete()
        return Response({"Message": "Scholarship deleted"}, status=status.HTTP_200_OK)
        
    
    
    def put(self,request,pk):
    
        try:
            scholar = Scholarship.objects.get(pk=pk)
        except Scholarship.DoesNotExist:
            return Response({"Message": "Scholarship doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, scholar)  # Check object-level permission
        seri = ScholarshipSerializer(partial=True ,instance=scholar, data=request.data)
        
        if seri.is_valid():
            seri.save()
            # if 'Error Message'in e: 
            #     return Response({"Message":e }, status=status.HTTP_200_OK)
                
            return Response({"Message": "Scholarship Updated Successfuly"}, status= status.HTTP_200_OK)
        else:
            return Response({"Message": "Error in validating data"}, status= status.HTTP_400_BAD_REQUEST)
        
            
        




@method_decorator(csrf_exempt, name='dispatch')
class ProviderScholarships(APIView):
    
    permission_classes= [isProvider,IsAuthenticated]
    def get(self,request):    
        
        scholars = Scholarship.objects.filter(provider_id = request.user.id)
        
        if scholars.count() ==1 :
            seri = ViewScholarshipSerializer(scholars.first())
        else:
            seri  = ViewScholarshipSerializer(scholars, many=True)
            
        
        return Response({"Message": seri.data}, status=status.HTTP_200_OK)



@method_decorator(csrf_exempt, name='dispatch')
class Favorite(APIView):
    
    permission_classes= [isSeeker,IsAuthenticated]
    def get(self,request):
        
        token = get_token(request)
        access = AccessToken(token)

        if request.method =="GET":
            
            scholars = Scholarship_Seeker.objects.filter(seeker= access.payload['id'])
            
            serialized_scholars = []
            for scholar in scholars:
                scholarship = Scholarship.objects.get(pk = scholar.scholarship.pk)
                serialized_scholar = ViewScholarshipSerializer(scholarship, context={'request': request}).data
                serialized_scholars.append(serialized_scholar)
                
                
            return Response(serialized_scholars)
        
        
    def post(self,request,pk):
            
        token = get_token(request)
        access = AccessToken(token)


        if request.method == "POST":
            data = request.data 
            data["seeker"] = access.payload['id']
            data["scholarship"] = pk
            
            seri = ViewScholarshipSeekerSerializer(data = data)
            
            
            if seri.is_valid():
                seri.save()
            else:
                return Response({"Message":"Invalid data, item haven't been saved"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"Message":"Scholarship has been added to favorite list "}, status=status.HTTP_202_ACCEPTED)
        
        
