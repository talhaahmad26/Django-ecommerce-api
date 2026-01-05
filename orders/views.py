from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Order,OrderItem,Cart,CartItem
from .serializers import OrderSerializer,CartSerializer,CartItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from products.models import Product
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin sabke orders dekh sake, Normal user sirf apne orders
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User ko sirf apni cart dikhni chahiye
        return Cart.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        # Naya item add karte waqt user set karein
        serializer.save(user=self.request.user)

        # --- ADD TO CART API (Custom Logic) ---
    @action(detail=False, methods=['post'])
    def add_to_cart(self,request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity',1))
        # 1. User ki cart dhundo, agar nahi hai to banao
        cart, created=Cart.objects.get_or_create(user=request.user)
        # 2. Check karo item pehle se cart mein hai ya nahi
        # (Yahan Product model import karna padega agar upar nahi kiya to)
        product = Product.objects.get(id=product_id)
        # 3. Item add ya update karo
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # Agar pehle se tha to quantity badha do
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        return Response({'message': 'Item added to cart', 'cart_id':cart.id})
    # --- CHECKOUT API (Cart -> Order) ---
    @action(detail=False, methods=['post'])
    def checkout(self,request):
        # 1. User ki cart nikalo
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error':'cart is empty'}, status=400)
        # 2. Naya Order banao
        order = Order.objects.create(
            user = request.user,
            status = 'Pending',
            shipping_address = request.data.get('address','Default Address'),
            total_price = 0
        )
        total_price = 0
        # 3. Cart ke items ko OrderItems mein convert karo
        for item in cart.items.all():
            if item.product.stock >= item.quantity:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                # Stock minus karo
                item.product.stock -= item.quantity
                item.product.save()

                total_price += item.product.price * item.quantity
            else:
                order.delete() # Agar stock nahi hai to order cancel
                return Response({'error':f"stock not available for {item.product.name}"}, status=400)
            # 4. Total save karo
        order.total_price = total_price
        order.save()
        # 5. Cart delete kar do (Kyunki order ban gaya)
        cart.delete()
        return Response({'message': 'Order placed Successfully', 'order_id': order.id})
