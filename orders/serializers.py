
from rest_framework import serializers
from .models import Order, OrderItem,Cart,CartItem
from django.db import transaction  # <--- 1. Ye import zaroor karein (Safety ke liye)

class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.ReadOnlyField(source='product.price')
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    grand_total = serializers.SerializerMethodField()  # Total price hum calculate karenge

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'grand_total']

        # Yeh function cart ka total bill calculate karega
    def get_grand_total(self,obj):
        total = 0
        for item in obj.items.all():
            total += item.product.price * item.quantity
        return total

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'shipping_address', 'created_at', 'items']
        read_only_fields = ['user', 'status', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # 'atomic' ka matlab hai: Ya to poora order save ho, ya kuch bhi na ho.
        # Aisa nahi hona chahiye ke paise kat gaye aur order fail ho gaya.
        with transaction.atomic():
            order = Order.objects.create(user=user, **validated_data)
            total_price = 0
            
            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                
                # --- VALIDATION CHECK (Ye Naya Hai) ---
                if product.stock < quantity:
                    # Agar stock kam hai to yahi ruk jao aur error do
                    raise serializers.ValidationError(
                        f"Sorry! {product.name} ka stock sirf {product.stock} bacha hai."
                    )
                # --------------------------------------

                price = product.price
                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
                
                total_price += price * quantity
                
                # Stock minus karo
                product.stock -= quantity
                product.save()
            
            order.total_price = total_price
            order.save()
            
        return order