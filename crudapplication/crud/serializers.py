from dataclasses import fields
from xml.parsers.expat import model
from rest_framework import serializers

from crud.models import UserProfile


class RegisterUserValidator(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(max_length=30, required=True)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(max_length=50, required=True)
    phone = serializers.CharField(max_length=10, required=True)
    city = serializers.CharField(max_length=32, required=True)
    country = serializers.CharField(max_length=32, required=True)
    address = serializers.CharField(max_length=255, required=True)
    device_type = serializers.CharField(max_length=10, required=True)
    zipcode = serializers.IntegerField(required=True)


class LoginUserValidator(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class GetUserValidator(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)


class UserprofileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_email(self, obj):
        return obj.user.email

    def get_username(self, obj):
        return obj.user.username