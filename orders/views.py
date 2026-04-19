from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from cart.models import CartItem, Cart
from .models import Order, OrderItem


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        order = Order.objects.create(user=request.user, total_price=0)

        total_price = 0

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total_price += item.product.price * item.quantity

        order.total_price = total_price
        order.save()

        # clear cart
        cart_items.delete()

        return Response({"message": "Order placed successfully"})