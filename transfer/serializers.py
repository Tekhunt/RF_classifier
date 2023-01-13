from rest_framework import serializers
from transfer.models.account import Account
from transfer.models.deposit_model import Deposit
from transfer.models.transaction import Transaction
from transfer.models.user_model import CustomUser
from django.contrib.auth import authenticate

# from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super.update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ("id", "name", "email", "password", "balance")
#         extra_kwargs = {"password": {"write_only": True}}


# class AuthTokenSerializer(serializers.Serializer):
#     email = serializers.CharField()
#     password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         user = authenticate(
#             request=self.context.get('request'),
#             email=email,
#             password=password
#         )
#         if not user:
#             msg = 'Unable to authenticate with provided credentials'
#             raise serializers.ValidationError(msg, code='authentication')

#         attrs['user'] = user
#         return attrs


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ("id", "account" "amount", "timestamp")


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "client", "balance", "timestamp")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "sender", "recipient", "amount", "timestamp")
