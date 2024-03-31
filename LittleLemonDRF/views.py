
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from .models import Category, MenuItem
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinutes
from django.contrib.auth.models import User, Group

# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price','inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message:some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"msg":"Only managers should see this"})
    else:
        return Response({"msg":"You're not authorized"},403)

@api_view()
@throttle_classes([AnonRateThrottle]) #for anonymous users
def throttle_check(request):
    return Response({"msg":"successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinutes])
def throttle_check_auth(request):
    return Response({"msg":"for logged in users only"})

#api endpoint for super admin only that he can assign a user to a group 
@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
            return Response({"msg":"user added to manager group"})
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
            return Response({"msg":"user deleted to manager group"})
    return Response({"msg":"ok"})