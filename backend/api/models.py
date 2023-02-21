from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel


class ExternalLink(models.Model):
    text = models.CharField(max_length=20)
    url = models.URLField()


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)


class Event(models.Model):
    name = models.TextField(null=False, blank=False)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    ticketStart = models.DateTimeField(null=True, blank=True)
    ticketEnd = models.DateTimeField(null=True, blank=True)
    ticketLimit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Perk(models.Model):
    text = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    tooltip = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text


class Ticket(models.Model):
    TYPE_STANDARD = "standard"
    TYPE_MEMBERSHIP = "membership"
    TYPES = [(TYPE_STANDARD, "Standard"), (TYPE_MEMBERSHIP, "Membership")]

    name = models.TextField(blank=False, null=False)
    validUntil = models.DateTimeField(blank=False, null=False)
    validFrom = models.DateTimeField(blank=False, null=False)
    type = models.CharField(max_length=32, choices=TYPES, null=False, blank=False)
    price = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    perks = models.ManyToManyField(Perk)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.get_full_name()

    def __unicode__(self):
        return self.get_full_name()


class Product(PolymorphicModel):
    value = models.IntegerField(default=0)


class ProductTicket(Product):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    name = models.TextField(blank=False, null=False, default="")

    def __unicode__(self):
        return f"{self.ticket.name} ({self.name})"

    def __str__(self):
        return f"{self.ticket.name} ({self.name})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total = models.IntegerField(default=0, null=False, blank=False)
    is_payed = models.BooleanField(default=False)

    def __unicode__(self):
        return f"#{self.id}"

    def __str__(self):
        return f"#{self.id}"


class Quota(models.Model):
    year = models.PositiveBigIntegerField(null=False, blank=False)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)


class Badge(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)
    website = models.CharField(blank=True, null=True, default=None, max_length=200)


class Location(models.Model):
    TYPE_ROOM = "room"
    TYPE_SHELF = "shelf"
    TYPES = [(TYPE_ROOM, "Room"), (TYPE_SHELF, "Shelf")]

    name = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=32, choices=TYPES, default=TYPE_SHELF)

    def __str__(self):
        return self.name


class BggGame(models.Model):
    bggid = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)

    badges = models.ManyToManyField(Badge, blank=True, default=None)

    rank = models.IntegerField(null=True)
    min_players = models.IntegerField(null=True)
    max_players = models.IntegerField(null=True)
    min_playtime = models.IntegerField(null=True)
    max_playtime = models.IntegerField(null=True)
    thumbnail = models.CharField(blank=True, max_length=500, default="")
    image = models.CharField(blank=True, max_length=500)
    other_names = models.JSONField(blank=True, default=list)
    year = models.CharField(blank=True, max_length=10, default="", null=True)

    @staticmethod
    def most_withdraws(number):
        return (
            Withdraw.objects.all()
            .values("game__game__name", "game__game__image")
            .annotate(total=Count("game"))
            .order_by("-total")[:number]
        )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Game(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    game = models.ForeignKey(BggGame, null=True, blank=True, on_delete=models.CASCADE)

    notes = models.TextField(blank=True)
    date_checkin = models.DateTimeField(default=None, blank=True, null=True)
    date_checkout = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s" % self.game.name

    def __str__(self):
        return self.game.name


class LibraryGame(Game):
    location = models.ForeignKey(
        Location, null=True, blank=True, default=None, on_delete=models.CASCADE
    )

    def status(self):
        if not self.location or self.date_checkin is None:
            return "not-checked-in"
        elif self.date_checkout is not None:
            return "checked-out"
        elif self.withdraw_set.filter(date_returned=None).count() == 0:
            return "available"
        else:
            return "not-available"

    def current_withdraw(self):
        if self.status() == "not-available":
            return self.withdraw_set.filter(date_returned=None).first()
        else:
            return None

    def save(self, *args, **kwargs):
        if self.location and not self.date_checkin:
            self.date_checkin = timezone.now()

        super().save()


class UsedGame(Game):
    price = models.FloatField(default=0.0, blank=False, null=False)


class StoreGame(models.Model):
    game = models.ForeignKey(BggGame, null=True, blank=True, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, null=True, blank=True, on_delete=models.CASCADE
    )
    selling_price = models.FloatField(default=0.0, blank=False, null=False)
    discount_price = models.FloatField(default=0.0, blank=False, null=False)
    stock = models.IntegerField(default=0, blank=False, null=False)


class Withdraw(models.Model):
    requisitor = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    game = models.ForeignKey(LibraryGame, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date_withdrawn = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(default=None, blank=True, null=True)

    def returned(self):
        return self.date_returned is not None

    # returned.boolean = True
    def duration(self):
        date_returned = (
            self.date_returned.replace(tzinfo=None)
            if self.date_returned
            else datetime.now().replace(tzinfo=None)
        )

        return date_returned - self.date_withdrawn.replace(tzinfo=None)

    def __unicode__(self):
        return self.requisitor.get_full_name()

    def __str__(self):
        return self.requisitor.get_full_name()

    @staticmethod
    def last(days):

        items = (
            Withdraw.objects.filter(
                date_withdrawn__range=(
                    datetime.now() - timedelta(days=days),
                    datetime.now(),
                )
            )
            .extra({"date_withdrawn": "date(date_withdrawn)"})
            .values("date_withdrawn")
            .annotate(created_count=Count("id"))
        )

        items = list(items)

        dates = [x.get("date_withdrawn") for x in items]

        for d in (datetime.today() - timedelta(days=x) for x in range(0, days)):
            if d.date().isoformat() not in dates:
                items.append(
                    {"date_withdrawn": d.date().isoformat(), "created_count": 0}
                )

        items.sort(key=lambda o: o["date_withdrawn"])
        return items
