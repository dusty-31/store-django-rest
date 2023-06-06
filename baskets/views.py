from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Product

from .models import Basket, BasketLine
from .serializers import BasketSerializer, BasketLineSerializer
from .permissions import IsOwner


class BasketAPIView(APIView):
    permission_classes = [IsOwner, ]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            baskets = Basket.objects.filter(owner=request.user)
            serializer = BasketSerializer(instance=baskets, many=True)
            response_key = 'baskets'
        else:
            basket = Basket.objects.get(pk=pk)
            serializer = BasketSerializer(basket)
            response_key = 'basket'
        return Response({response_key: serializer.data})

    def post(self, request, *args, **kwargs):
        request.data['owner'] = request.user.username
        serializer = BasketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'new_basket': serializer.data})
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})
        instance = get_object_or_404(klass=Basket, pk=pk)
        if instance.status == Basket.Status.SUBMITTED.name:
            return Response({'error': 'You cannot change a basket that has been submitted.'})
        serializer = BasketSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response({'updated_basket': serializer.data})
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class BasketLineAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BasketLineSerializer(data=request.data)
        if serializer.is_valid():
            basket = get_object_or_404(klass=Basket, pk=serializer.validated_data['basket']['id'])

            if basket.status in [Basket.Status.FROZEN.name, Basket.Status.SUBMITTED.name]:
                return Response({'error': 'Cannot add product to a frozen or submitted basket.'},
                                status=status.HTTP_403_FORBIDDEN)

            product = Product.objects.get(pk=serializer.validated_data['product']['id'])
            if product.quantity < serializer.validated_data['quantity']:
                return Response({'error': 'Transferred quantity exceeds the quantity in the warehouse'},
                                status=status.HTTP_403_FORBIDDEN)

            existing_basket_line = BasketLine.objects.filter(basket=request.data['basket'],
                                                             product=request.data['product']).first()
            if existing_basket_line:
                new_quantity = existing_basket_line.quantity + int(request.data['quantity'])
                if product.quantity < new_quantity:
                    return Response({'error': 'Updated quantity exceeds the quantity in the warehouse'},
                                    status=status.HTTP_403_FORBIDDEN)

                existing_basket_line.quantity = new_quantity
                existing_basket_line.save()
                serializer = BasketLineSerializer(existing_basket_line)
                return Response({'updated_basket_line': serializer.data})

            serializer.save()
            return Response({'new_basket_line': serializer.data})

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed.'})
        instance = get_object_or_404(klass=BasketLine, pk=pk)
        serializer = BasketLineSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response({'updated_basket_line': serializer.data})
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
