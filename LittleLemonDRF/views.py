
from django.shortcuts import render
from rest_framework import generics
from .models import Category, MenuItem
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


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