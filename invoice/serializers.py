from django.core.exceptions import ValidationError
from rest_framework import serializers

from invoice.models import Order, OrderItem, SHOPPING
from products.models import Product, CLOTH, SPORT_TOOL, Cloth, SportTool


class OrderItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'count',
            'size',
            'color'
        ]

    def validate(self, attrs):
        if attrs.get('product').type == CLOTH:
            product = Cloth.objects.get(id=attrs.get('product').id)
        else:
            product = SportTool.objects.get(id=attrs.get('product').id)

        if attrs.get('count') < 1:
            raise ValidationError("Sorry! Invalid count number!")

        if attrs.get('product').amount - attrs.get('count') < 0:
            raise ValidationError("Sorry! " + attrs.get('product').title + " is not available enough")
        if attrs.get('color') not in attrs.get('product').color.all():
            raise ValidationError("Invalid color")
        if attrs.get('size') not in product.size.all():
            raise ValidationError("Invalid size")

        qs = OrderItem.objects.filter(order__user=self.context.get('request').user, order__state=SHOPPING,
                                      product__id=product.id, color=attrs.get('color'), size=attrs.get('size'))
        if qs.exists():
            raise ValidationError("This item is already in your cart with the same info")

        attrs['price'] = attrs.get('product').price
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        product = instance.product
        product.amount -= 1
        product.save()
        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'count',
            'price',
            'size',
            'color'
        ]

    def get_size(self, obj):
        return obj.size.size

    def get_color(self, obj):
        return obj.color.name

    def get_product(self, obj):
        if obj.product.type == CLOTH:
            cloth = Cloth.objects.get(id=obj.product.id)
            return {
                "id": cloth.id,
                "title": cloth.title,
                "picture": cloth.pictures.first().picture.url
            }
        elif obj.product.type == SPORT_TOOL:
            sport_tool = SportTool.objects.get(id=obj.product.id)
            return {
                "id": sport_tool.id,
                "title": sport_tool.title,
                "picture": sport_tool.pictures.first().picture.url
            }


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'date',
            'state',
            'items'
        ]
