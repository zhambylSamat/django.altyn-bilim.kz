from rest_framework import serializers
from userInfo.api.serializers import StudentSerializer
from django.contrib.auth.models import User
from userInfo.models import Student
from django.contrib.auth.hashers import check_password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=120)
    password = serializers.CharField(min_length=7, max_length=120)


class ChangePasswordSerilizer(serializers.Serializer):
    user = serializers.IntegerField()
    old_password = serializers.CharField(max_length=120)
    new_password = serializers.CharField(max_length=120)
    confirm_password = serializers.CharField(max_length=120)

    def validate(self, attrs):
        try:
            user = User.objects.get(pk=attrs['user'])
            if not check_password(attrs['old_password'], user.password):
                raise serializers.ValidationError("Бұрынғы қүпия сөз қате енгізілген")
            elif len(attrs['new_password']) <= 6:
                raise serializers.ValidationError("Жаңа қүпия сөздің ұзындығы 7-ден кем болмауы керек")
            elif attrs['new_password'] != attrs['confirm_password']:
                raise serializers.ValidationError("Жаңа пароль ұқсамайды")

            return attrs
        except User.DoesNotExist:
            raise serializers.ValidationError('Бүндай қолданушы базадан табылмады')


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)

    def get_role(self, user):
        return user.user_role.get().role

    # def update(self, instance, validated_data):
    #     try:
    #         student_data = validated_data.pop('student')
    #         Student.objects.filter(user__pk=instance.pk).update(**student_data)
    #     except KeyError:
    #         pass
    #
    #     User.objects.filter(pk=instance.pk).update(**student_data)
    #     user = User.objects.get(pk=instance.pk)
    #     return user

    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name', 'email', 'role')
        extra_kwargs = {'username': {'allow_blank': True}}

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        try:
            student = instance.user_student.get()
            data['student'] = StudentSerializer(student, many=False).data
        except Student.DoesNotExist:
            pass
        return data


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name', 'email')
