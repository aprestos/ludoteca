from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin

from backend.api.models import (
    Badge,
    BggGame,
    Event,
    ExternalLink,
    LibraryGame,
    Location,
    Order,
    PaymentMethod,
    Perk,
    Product,
    ProductTicket,
    Quota,
    Ticket,
    Withdraw,
)
from backend.api.signals import payment_confirmed

User = get_user_model()

admin.site.register(User, UserAdmin)


@admin.register(ExternalLink)
class LibraryGameAdmin(admin.ModelAdmin):
    search_fields = ["text", "url"]
    list_display = (
        "text",
        "url",
    )


@admin.register(PaymentMethod)
class LibraryGameAdmin(admin.ModelAdmin):
    search_fields = ["name", "value"]
    list_display = (
        "name",
        "value",
    )


@admin.register(BggGame)
class BggGameAdmin(admin.ModelAdmin):
    fields = ("name", "bggid", "badges")
    list_display = ("name", "bggid", "rank")
    readonly_fields = (
        "bggid",
        "name",
    )
    ordering = ("name",)


admin.site.register(Badge)


@admin.register(LibraryGame)
class LibraryGameAdmin(admin.ModelAdmin):
    search_fields = ["game__name", "notes"]
    list_display = (
        "game",
        "owner",
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    ordering = ("name", "type")


@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ("game", "requisitor", "duration")
    ordering = ("game", "requisitor")


@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display = ("user", "year")
    ordering = ("-year", "user")
    search_fields = ["user__first_name", "user__last_name"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "user", "total", "is_payed", "is_sent")
    readonly_fields = ("user", "products", "total")
    ordering = ("id",)
    search_fields = ["id", "code", "user__first_name", "user__last_name", "user__email"]

    def save_model(self, request, obj, form, change):
        res = Order.objects.get(pk=obj.pk)
        if not res.is_payed and obj.is_payed:
            payment_confirmed.send(sender=self.__class__, instance=self, order=obj)
        super().save_model(request, obj, form, change)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    ordering = ("type",)


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    ordering = ("ticket__type",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin):
    child_models = (ProductTicket,)
    ordering = ("id",)


@admin.register(ProductTicket)
class ProductTicketAdmin(PolymorphicChildModelAdmin):
    search_fields = ["id", "name"]
    list_display = ("id", "name", "get_ticket_type", "get_ticket_price", "get_orders")
    ordering = ("name",)
    show_in_index = True

    @admin.display(description="Ticket")
    def get_ticket_type(self, obj: ProductTicket):
        return obj.ticket.type

    @admin.display(description="Price")
    def get_ticket_price(self, obj: ProductTicket):
        return obj.ticket.price

    @admin.display(description="Order")
    def get_orders(self, obj: ProductTicket):
        return [order.id for order in obj.order_set.all()]
