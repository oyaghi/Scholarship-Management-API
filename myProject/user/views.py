from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Provider, CustomUser, Seeker
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import Group


@api_view(['POST'])
@csrf_exempt
def register(request):
    data = JSONParser().parse(request)
    if request.method == 'POST':
        
        if 'work_email' in data :

            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            work_email = data['work_email']
            password = data['password']


            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)

            group = Group.objects.get(name='Provider')

            # Add the user to the group
            group.user_set.add(user)

            user.is_provider = True
            user.save()
            provider = Provider.objects.create(user=user, work_email=work_email)
            
            # user = CustomUser.objects.get(email='user16@example.com')

            # # Check if the user is a member of the `Provider` group
            # if user.groups.filter(name='Provider').exists():
            #     print('User is a member of the `Provider` group')
            # else:
            #     print('User is not a member of the `Provider` group')
            
            return Response({'message': 'Provider registered successfully!'})
        
        elif 'ed_level' in data:
            
            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            ed_level = data['ed_level']
            password = data['password']


            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)

            group = Group.objects.get(name='Provider')

            # Add the user to the group
            group.user_set.add(user)

            user.is_seeker = True
            user.save()
            seeker = Seeker.objects.create(user=user, ed_level=ed_level)

            return Response({'message': 'Seeker registered successfully!'})
        
            

    else:
        return Response({'message': 'Invalid request method'})