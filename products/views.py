from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsAdminOrSellerReadOnly, IsAdminOrReadOnly


class CategoryAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly, ]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            response_key = 'categories'
        else:
            category = get_object_or_404(klass=Category, pk=pk)
            serializer = CategorySerializer(category)
            response_key = 'category'
        return Response({response_key: serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'new_category': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class ProductAPIView(APIView):
    permission_classes = [IsAdminOrSellerReadOnly, ]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            response_key = 'products'
        else:
            product = get_object_or_404(klass=Product, pk=pk)
            serializer = ProductSerializer(product)
            response_key = 'product'

        return Response({response_key: serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not request.data.get('owner', None):
            data = request.data.copy()
            data['owner'] = request.user.username
        else:
            data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'new_product': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance = get_object_or_404(klass=Product, pk=pk)
        self.check_object_permissions(request=request, obj=instance)
        serializer = ProductSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response({'updated_product': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
