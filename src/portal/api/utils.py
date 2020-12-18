from rest_framework.response import Response
from portal.api.serializer import UserSerializer
import json
from oauth2_provider.models import AccessToken, RefreshToken
from django.conf import settings
from django.contrib.auth.models import User
import requests
from django.core.exceptions import PermissionDenied
from userInfo.models import UserRole
from string import ascii_lowercase, digits
from random import choice
import datetime

USER_DOES_NOT_EXISTS = "`Пайдаланушының аты` емесе `Қүпия сөз` қате енгізілген"
USERNAME_OR_PASSWORD_ERROR = "`Пайдаланушының аты` емесе `Қүпия сөз` қате енгізілген"


def user_does_not_exists():
    result = {
        "errors": [
            USER_DOES_NOT_EXISTS
        ]
    }
    return Response(result, status=404)


def wrong_username_or_password():
    result = {
        "errors": [
            USERNAME_OR_PASSWORD_ERROR
        ]
    }
    return Response(result, status=404)


def get_user_response(user, password=None):
    result = {}
    userSerializer = UserSerializer(user)

    userJson = json.loads(json.dumps(userSerializer.data))
    result['user'] = userJson
    result['token'] = revoke_and_get_token(user.username, password)
    return result


def revoke_token(username):
    try:
        access_tokens = AccessToken.objects.filter(user=User.objects.get(username=username))
        url = settings.BASE_URL + 'o/revoke_token/'
        for token in access_tokens:
            data = {
                'token': token.token,
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.CLIENT_SECRET,
            }
            requests.post(url, data)
        RefreshToken.objects.filter(access_token_id=None).delete()
    except:
        pass


def revoke_and_get_token(username, password=None):
    try:
        access_tokens = AccessToken.objects.filter(user=User.objects.get(username=username))
        url = settings.BASE_URL + 'o/revoke_token/'
        for token in access_tokens:
            data = {
                'token': token.token,
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.CLIENT_SECRET,
            }
            requests.post(url, data)
        RefreshToken.objects.filter(access_token_id=None).delete()
    except:
        pass

    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
    }
    url = settings.BASE_URL + 'o/token/'
    response = requests.post(url, data=data,)
    return response.json()


def permission(roles=None, user=None):
    if not roles or not user:
        raise PermissionDenied
    try:
        role = UserRole.objects.get(user__pk=user.pk)
        if role.role not in roles:
            raise PermissionDenied
    except UserRole.DoesNotExist:
        raise PermissionDenied


def generate_random_username(length=16, chars=ascii_lowercase+digits, split=4, delimer='-'):

    username = ''.join([choice(chars) for i in range(length)])

    if split:
        username = delimer.join([username[start:start+split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimer=delimer)
    except User.DoesNotExist:
        return username


def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + (date.month+delta-1) // 12
    if not m:
        m = 12
    d = min(date.day, [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m-1])
    return date.replace(day=d, month=m, year=y)


def get_day_id_from_date(date):
        day_id = int(date.strftime('%w'))
        day_id = 7 if day_id == 0 else day_id
        return int(day_id)


def increase_one_day_in_date(date):
    return date + datetime.timedelta(days=1)


def decrease_one_day_in_date(date):
    return date - datetime.timedelta(days=1)


def delete_ent_list(user_pk, ent_list):
    for ent in ent_list:
        ent.delete(user_pk=user_pk)


def delete_ent(user_pk, ent):
    ent.delete(user_pk)
