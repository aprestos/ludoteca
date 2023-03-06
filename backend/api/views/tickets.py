import json
from io import BytesIO

import qrcode
import qrcode.image.svg
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from rest_framework.views import APIView

from backend.api.models import Order
from backend.api.utils.utils import get_base_email_context, send_mail


class SendTicketsViewSet(APIView):
    def post(self, request):
        body = {}
        if request.body:
            body = json.loads(request.body)

        if "emails" in body and type(body["emails"]) == list:
            query = Order.objects.filter(user__email__in=body["emails"])[:1]
        else:
            query = Order.objects.filter(is_sent=False, is_payed=True).all()[:20]

        for order in query:
            context = get_base_email_context()
            tickets = []
            qrcode_text = ""

            for product in order.products.all():
                ticket = {
                    "number": product.id,
                    "name": product.name,
                    "type": product.ticket.name,
                }

                qrcode_text += f"{product.name} - {product.ticket.name}\n"

                tickets.append(ticket)
                context.update({"tickets": tickets})

            if not order.code:
                code = get_random_string(length=5).upper()
                order.code = code

            context.update({"code": order.code})

            factory = qrcode.image.svg.SvgImage
            img = qrcode.make(
                f"Order #{order.id} - {order.user.get_full_name()} ({len(order.products.all())})\n"
                + qrcode_text,
                image_factory=factory,
                box_size=20,
            )
            stream = BytesIO()
            img.save(stream)
            context["svg"] = stream.getvalue().decode()

            send_mail(
                to=order.user.email,
                context=context,
                subject="Your tickets are here!",
                template="email/tickets.html",
            )
            order.is_sent = True
            order.save()
        return HttpResponse()
