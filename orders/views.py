from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PaymentMethod
from .serializers import OrderSerializer, PaymentMethodSerializer


class CheckoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.data.get('owner', None):
            data = request.data.copy()
            data['owner'] = request.user.pk
        else:
            data = request.data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'order': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class PaymentMethodAPIView(APIView):
    def get(self, request, *args, **kwargs):
        payment_methods = PaymentMethod.objects.all()
        serializer = PaymentMethodSerializer(payment_methods, many=True)
        return Response({'payment_methods': serializer.data})


class ShippingDetailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        pass


class PaymentDetail(APIView):
    def post(self, request, *args, **kwargs):
        pass


class PaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        pass
