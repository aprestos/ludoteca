import logging

from django.core import serializers
from django.core.mail import EmailMessage
from django.dispatch import Signal, receiver
from django.template.loader import get_template
from django_rest_passwordreset.signals import reset_password_token_created
from dotenv import find_dotenv, load_dotenv

from backend.api.models import PaymentMethod
from backend.api.utils import environment

load_dotenv(find_dotenv())  # loads the configs from .env
# reading .env file


user_created = Signal()

new_order = Signal()

payment_confirmed = Signal()


def extract_reset_token_data(data):
    return {
        "current_user": serializers.serialize("json", [data.user]),
        "user_first_name": data.user.first_name,
        "username": data.user.username,
        "email": data.user.email,
        "reset_password_url": f"{environment.get_reset_password_url()}{data.key}",
        "logo_url": environment.get_logo_url(),
        "name": environment.get_app_name(),
        "app_url": environment.get_app_url(),
    }


def send_mail(to: str, context, subject: str, template: str):
    try:
        msg = EmailMessage(
            subject,
            body=get_template(template).render(context),
            from_email="info@leiriacon.pt",
            to=[to],
            reply_to=["info@spielportugal.org"],
        )
        msg.content_subtype = "html"
        msg.send()

    except Exception as err:
        logging.error(err)
        raise err


@receiver(reset_password_token_created)
def send_password_url_by_mail(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    logging.info("Received reset_password_token_created signal")

    context = extract_reset_token_data(reset_password_token)

    send_mail(
        reset_password_token.user.email,
        context,
        subject=f"Reset your {environment.get_app_name()} password",
        template="email/password_reset.html",
    )


@receiver(user_created)
def send_password_url_by_mail_to_new_user(
    sender, instance, reset_password_token, *args, **kwargs
):
    context = extract_reset_token_data(reset_password_token)

    # send an e-mail to the user
    logging.info("Received user_created signal")
    send_mail(
        reset_password_token.user.email,
        context,
        subject=f"Welcome to {environment.get_app_name()}'s portal",
        template="email/welcome.html",
    )


@receiver(new_order)
def send_new_order_email(sender, instance, order, *args, **kwargs):

    # send an e-mail to the user
    logging.info("Received user_created signal")

    context = {
        "logo_url": environment.get_logo_url(),
        "name": environment.get_app_name(),
        "user": serializers.serialize("json", [order.user]),
        "order_number": order.id,
        "order_total": order.total / 100,
        "payment_methods": [
            {"name": method.name, "value": method.value}
            for method in PaymentMethod.objects.all()
        ],
        "products": [
            {
                "name": product.name,
                "type": product.ticket.name,
                "value": product.value / 100,
            }
            for product in order.products.all()
        ],
    }

    send_mail(
        order.user.email,
        context=context,
        subject=f"{environment.get_app_name()} - Order confirmation",
        template="email/order-summary.html",
    )


@receiver(payment_confirmed)
def send_payment_confirmation(sender, instance, order, *args, **kwargs):
    context = {
        "logo_url": environment.get_logo_url(),
        "name": environment.get_app_name(),
        "user": serializers.serialize("json", [order.user]),
        "order_number": order.id,
        "order_total": order.total / 100,
        "products": [
            {
                "name": product.name,
                "type": product.ticket.name,
                "value": product.value / 100,
            }
            for product in order.products.all()
        ],
    }

    # send an e-mail to the user
    logging.info("Received payment_confirmed signal")
    send_mail(
        order.user.email,
        context,
        subject=f"{environment.get_app_name()} - Payment confirmation",
        template="email/receipt.html",
    )
