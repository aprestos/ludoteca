import django.core.exceptions
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from backend.api.models import Order, Product, ProductTicket, Ticket
from backend.api.signals import new_order

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("value",)


class ProductTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTicket
        fields = ("value", "ticket", "name")


class ProductPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Product: ProductSerializer,
        ProductTicket: ProductTicketSerializer,
    }


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.ListSerializer(child=ProductPolymorphicSerializer())

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        products = validated_data.pop("products")

        has_membership_ticket = False

        if not self.context["request"].user.is_staff:
            orders = Order.objects.filter(user__id=validated_data.get("user").id)
            if len(orders) > 1:
                raise django.core.exceptions.PermissionDenied(
                    "This user already bought tickets"
                )

            for product in products:
                if product.get("ticket", Ticket()).type == Ticket.TYPE_MEMBERSHIP:
                    if has_membership_ticket:
                        raise django.core.exceptions.BadRequest(
                            "Only one membership ticket per account is allowed"
                        )
                    else:
                        user: User = validated_data.get("user", User())
                        if (
                            not user
                            or not user.groups.filter(name="Associate").exists()
                        ):
                            raise django.core.exceptions.BadRequest(
                                "Only members can buy membership tickets"
                            )
                        else:
                            has_membership_ticket = True

        order = Order.objects.create(**validated_data)

        for product in products:
            resource_type = product.pop("resourcetype")
            if resource_type == "ProductTicket":
                value = product.get("ticket").price
                order.total += value
                p: ProductTicket = ProductTicket.objects.create(**product)
                p.value = value
                p.save()
                order.products.add(p)
                order.save()

        new_order.send(sender=self.__class__, instance=self, order=order)
        return order
