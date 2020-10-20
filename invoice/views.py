from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from invoice.models import Order, OrderItem, SHOPPING, PENDING
from invoice.serializers import OrderItemCreateSerializer, OrderItemSerializer, OrderSerializer


class AddItemToCartAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemCreateSerializer
    queryset = OrderItem.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        qs = user.orders.filter(state=SHOPPING)
        if qs.exists():
            serializer.save(order=qs.first())
        else:
            serializer.save(order=Order.objects.create(user=user))


class GetUserCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = request.user.orders.filter(state=SHOPPING)
        if qs.exists():
            return Response(OrderItemSerializer(qs.first().items, many=True).data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class SubmitOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = Order.objects.filter(user=user, state=SHOPPING)
        if qs.exists() and len(qs.first().items.all()) != 0:
            order = qs.first()
            order.state = PENDING
            order.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        return Response("No active order", status=status.HTTP_400_BAD_REQUEST)


class RemoveOrderItemAPIView(APIView):
    def delete(self, request, order_item_id):
        user = request.user
        qs = Order.objects.filter(user=user, state=SHOPPING)
        if qs.exists():
            order = qs.first()
            order_item = get_object_or_404(OrderItem, id=order_item_id)
            if order_item.order == order:
                product = order_item.product
                product.amount += 1
                product.save()
                order_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response("Item does not belong to active order", status.HTTP_400_BAD_REQUEST)
        return Response("No active order", status=status.HTTP_400_BAD_REQUEST)


class GetOrdersAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Order.objects.filter(user=self.request.user).exclude(state=SHOPPING).order_by('-date')
        return qs
