from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response
from ..models import Student
from portal.api.constants import ROLE_CHOICES
from portal.api.utils import user_does_not_exists
from portal.api.constants import ROLES_INFO, YOU_DON_NOT_HAVE_PERMISSION

USERNAME_EXIST_MESSAGE = "Бүндай username-мен ({}) тігкелген қолданушы базада бар. Баска username жазып көріңіз"
PHONE_EXISTS_MESSAGE = "Бүндай ұялы телефон нөмірі ({}) базада тігкелген. Басқа төмірді көріңіз"
ROLE_ERROR = "Role error please choose correct role"

def student_verification(student_request):
    messages = username_verification(student_request['user']['username'], student_request['user']['pk'])
    messages += student_phone_verification(student_request['student']['phone'], student_request['student']['pk'])

    if messages:
        return Response({'message': messages}, status=400)
    pass


def username_verification(username, user_pk=None):
    messages = []
    if user_pk:
        username_count = User.objects.filter(~Q(pk=user_pk)
                                             & (Q(username=username))).count()
    else:
        username_count = User.objects.filter(Q(username=username)).count()

    if username_count > 0:
        messages.append(USERNAME_EXIST_MESSAGE.format(username))

    return messages


def student_phone_verification(phone, student_pk=None):
    messages = []
    if student_pk:
        student = Student.objects.filter(~Q(pk=student_pk) & Q(phone=phone))
        # print(student[0].pk, student[0].phone)
        student_count = student.count()
    else:
        student_count = Student.objects.filter(Q(phone=phone)).count()

    if student_count > 0:
        messages.append(PHONE_EXISTS_MESSAGE.format(phone))
    return messages


def role_verification(role):
    messages = []
    if role in ROLE_CHOICES:
        messages.append(ROLE_ERROR)
    return messages


def staff_verification(staff_request):
    messages = username_verification(staff_request['user']['username'], staff_request['user']['pk'])
    messages += role_verification(staff_request['user']['role'])

    if messages:
        return Response({'message': messages}, status=400)
    pass


def access_to_edit_profile(user_pk, owner, edited_user_role=None):
    messages = []
    try:
        user = User.objects.get(pk=user_pk)
        user_level = find_level_by_prefix(user.user_role.get().role)
        owner_level = find_level_by_prefix(owner.user_role.get().role)
        changed_level = find_level_by_prefix(edited_user_role) if edited_user_role else None
        if changed_level:
            if owner_level >= changed_level:
                messages.append(YOU_DON_NOT_HAVE_PERMISSION)
                return Response({'message': messages}, status=400)
            else:
                pass
        elif user.pk == owner.pk:
            pass
        elif user_level > owner_level:
            pass
        else:
            messages.append(YOU_DON_NOT_HAVE_PERMISSION)
            return Response({'message': messages}, status=400)
    except User.DoesNotExist:
        return user_does_not_exists()


def access_to_create_profile(owner, created_user_role):
    messages = []
    owner_level = find_level_by_prefix(owner.user_role.get().role)
    created_level = find_level_by_prefix(created_user_role)
    if owner_level >= created_level:
        messages.append(YOU_DON_NOT_HAVE_PERMISSION)
        return Response({'message': messages}, status=400)
    else:
        pass


def find_level_by_prefix(prefix):
    for i in range(1, len(ROLES_INFO)):
        if ROLES_INFO[i][0] == prefix:
            return ROLES_INFO[i][1]
    return None
