from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
import uuid

from users.models import User


def get_confirmation_code():
    return get_random_string(20, uuid.uuid4().hex)


def send_confirmation_code(request):
    user = get_object_or_404(
        User,
        username=request.data.get('username'),
    )
    user.confirmation_code = get_confirmation_code()
    user.save()
    send_mail(
        'данные для получения токена',
        f'Код подтверждения {user.confirmation_code}',
        'token@yamdb.ru',
        [request.data.get('email')],
    )
