from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.contrib.auth import authenticate
from transfer.models.account import Account
from transfer.models.deposit_model import Deposit
from transfer.models.transaction import Transaction
from transfer.models.user_model import CustomUser
from transfer.serializers import (
    # AuthTokenSerializer,
    AccountSerializer,
    DepositSerializer,
    TransactionSerializer,
    UserSerializer,
)
from rest_framework.authtoken.models import Token

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class HomeView(APIView):
    def get(self, request):
        content = {"message": "Welcome to paynow web aaplication!"}
        return Response(content)


class RegisterApi(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            account = Account(client=user)
            account.save()
            return Response(
                UserSerializer(user, context=self.get_serializer_context()).data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=10),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = CustomUser.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response


# @api_view(["POST"])
# def register(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)


# @api_view(['POST'])
# def login(request):
#     serializer = AuthTokenSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.validated_data['user']
#     token, created = Token.objects.get_or_create(user=user)
#     return Response({'token': token.key})

# @api_view(['GET'])
# def login(request, format=None):
#     content = {
#         'user': str(request.user),  # `django.contrib.auth.User` instance.
#         'auth': str(request.auth),  # None
#     }
#     return Response(content)


@api_view(["POST"])
def deposit(request):
    # deserialize request data
    serializer = DepositSerializer(data=request.data)
    if serializer.is_valid():

        # retrieve user and amount from serialized data
        # user = get_object_or_404(CustomUser, pk=serializer.validated_data["user"])
        amount = serializer.validated_data["amount"]
        print(amount)
        print("User is =>", user)

        # update user balance
        if request.user.is_authenticated:
            client = request.user.id
            client.balance += amount
            # client.save()
            print(client.balance)
        else:
            return Response({"message": "Not authenticated"})

        # create a new deposit object
        deposit = Deposit(account=user, amount=amount)
        deposit.save()

        # serialize and return updated user information
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
    return Response(serializer.errors, status=400)


class UsersData(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class User(generics.RetrieveDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class AccountData(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDelete(generics.RetrieveDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

@api_view(["POST"])
def transfer(request):
    # deserialize request data
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        # retrieve sender, recipient, and amount from serialized data
        sender = request.user
        recipient = get_object_or_404(
            CustomUser, pk=serializer.validated_data["recipient"]
        )
        amount = serializer.validated_data["amount"]

        # update sender and recipient balances
        sender.balance -= amount
        recipient.balance += amount
        sender.save()
        recipient.save()

        # create a new transaction object
        transaction = Transaction(sender=sender, recipient=recipient, amount=amount)
        transaction.save()

        # serialize and return updated user information
        sender_serializer = UserSerializer(sender)
        recipient_serializer = UserSerializer(recipient)
        return Response(
            {
                "sender": sender_serializer.data,
                "recipient": recipient_serializer.data,
            }
        )
    return Response(serializer.errors, status=400)
