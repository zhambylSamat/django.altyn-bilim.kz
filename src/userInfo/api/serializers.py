from rest_framework import serializers
from ..models import Student, Parent, Staff, StudentFreeze, StudentGroupFreeze
from django.contrib.auth.models import User


# from portal.api.serializer import UserSerializer


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = (
            'pk',
            'user',
            'student',
            'is_main',
            'phone',
            'created_date'
        )
        read_only_fields = ('pk', 'user', 'student')


class UserParentSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)
    parent = serializers.SerializerMethodField()

    @staticmethod
    def get_role(user):
        return user.user_role.get().role

    @staticmethod
    def get_parent(user):
        try:
            return ParentSerializer(user.user_parent.get()).data
        except AttributeError:
            return None

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'parent'
        )
        read_only_fields = ('pk',)

    def to_representation(self, instance):
        data = super(UserParentSerializer, self).to_representation(instance)
        result = {
            'parent': data.pop('parent'),
            'user': data
        }
        return result


class StudentParentSerializer(serializers.ModelSerializer):
    parents = serializers.SerializerMethodField()

    @staticmethod
    def get_parents(student):
        try:
            parents = student.student_parent.all().order_by('-is_main')
            parent_list = []
            for parent in parents:
                parent_list.append(UserParentSerializer(parent.user).data)
            return parent_list
        except AttributeError:
            return None

    class Meta:
        model = Student
        fields = ('pk',
                  'user',
                  'has_payment',
                  'has_contract',
                  'is_password_reset',
                  'gender',
                  'phone',
                  'certificate',
                  'dob',
                  'school',
                  'grade',
                  'home_phone',
                  'address',
                  'target_subject',
                  'target_from',
                  'instagram',
                  'parents',
                  'created_date')
        read_only_fields = ('pk', 'created_date', 'has_payment', 'has_contract', 'is_password_reset')
        extra_kwargs = {'parents': {'allow_null': True,
                                    'many': True}}


class UserStudentSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)
    student = serializers.SerializerMethodField()

    @staticmethod
    def get_role(user):
        return user.user_role.get().role

    @staticmethod
    def get_student(user):
        return StudentParentSerializer(user.user_student.get()).data

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'student'
        )
        read_only_fields = ('pk',)

    def to_representation(self, instance):
        data = super(UserStudentSerializer, self).to_representation(instance)
        result = {
            'student': data.pop('student'),
            'user': data
        }
        return result


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = (
            'pk',
            'dob',
            'is_password_reset',
            'created_date'
        )
        read_only_fields = ('pk', 'is_password_reset', 'created_date')
        extra_kwargs = {'dob': {'allow_null': True}}

    def create(self, validated_data):
        user = validated_data.pop('user')
        user_pk = validated_data.pop('user_pk')
        staff = Staff(**validated_data)
        staff.user = user
        staff.save(user_pk=user_pk)
        return staff

    def update(self, instance, validated_data):
        user_pk = validated_data.pop('user_pk')
        has_changes = False
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                has_changes = True
                setattr(instance, attr, value)
        if has_changes:
            instance.save(user_pk=user_pk)
        return instance


class UserStaffSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)
    staff = serializers.SerializerMethodField()

    @staticmethod
    def get_role(user):
        return user.user_role.get().role

    @staticmethod
    def get_staff(user):
        return StaffSerializer(user.user_staff.get()).data

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'staff'
        )
        read_only_fields = ('pk',)

    def to_representation(self, instance):
        data = super(UserStaffSerializer, self).to_representation(instance)
        result = {
            'staff': data.pop('staff'),
            'user': data,
        }
        return result


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'pk',
            'user',
            'has_payment',
            'has_contract',
            'is_password_reset',
            'grade',
            'phone',
            'certificate',
            'dob',
            'school',
            'home_phone',
            'address',
            'target_subject',
            'target_from',
            'instagram',
            'created_date'
        )
        read_only_fields = ('pk', 'user', 'created_date', 'has_payment', 'has_contract', 'is_password_reset')

    def create(self, validated_data):
        user = validated_data.pop('user')
        user_pk = validated_data.pop('user_pk')
        student = Student(**validated_data)
        student.user = user
        student.save(user_pk=user_pk)
        return student

    def update(self, instance, validated_data):
        user_pk = validated_data.pop('user_pk')
        has_changes = False
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                has_changes = True
                setattr(instance, attr, value)
        if has_changes:
            instance.save(user_pk=user_pk)
        return instance


class ParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parent
        fields = (
            'pk',
            'user',
            'student',
            'is_main',
            'phone',
            'created_date'
        )
        read_only_fields = ('pk', 'user', 'student', 'created_date')

    def create(self, validated_data):
        user = validated_data.pop('user')
        user_pk = validated_data.pop('user_pk')
        student = validated_data.pop('student')
        parent = Parent(**validated_data)
        parent.user = user
        parent.student = student
        parent.save(user_pk=user_pk)
        return parent

    def update(self, instance, validated_data):
        user_pk = validated_data.pop('user_pk')
        has_changes = False
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                has_changes = True
                setattr(instance, attr, value)
        if has_changes:
            instance.save(user_pk=user_pk)
        return instance


class StudentFreezeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentFreeze
        fields = (
            'pk',
            'student',
            'from_date',
            'to_date',
            'comment',
            'created_date'
        )

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        student_freeze = StudentFreeze(**validated_data)
        student_freeze.save(user_pk=user_pk)
        return student_freeze

    def update(self, instance, validated_data):
        user_pk = validated_data.pop('user_pk')
        has_changes = False
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                has_changes = True
                setattr(instance, attr, value)
        if has_changes:
            instance.save(user_pk=user_pk)
        return instance


class StudentGroupFreezeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentGroupFreeze
        fields = (
            'pk',
            'lesson_group_student',
            'date',
            'comment'
        )

    def create(self, validated_data):
        user_pk = validated_data.pop('user_pk')
        student_group_freeze = StudentGroupFreeze(**validated_data)
        student_group_freeze.save(user_pk=user_pk)
        return student_group_freeze

    def update(self, instance, validated_data):
        user_pk = validated_data.pop('user_pk')
        has_changes = False
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                has_changes = True
                setattr(instance, attr, value)
        if has_changes:
            instance.save(user_pk=user_pk)
        return instance
