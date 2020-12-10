from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'groups']
        extra_kwargs = {'password': {'write_only': True}}

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']

class ChangePassSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserAdminEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups']

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        


