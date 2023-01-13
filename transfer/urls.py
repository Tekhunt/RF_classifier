from django.urls import path
from transfer.views import (
    AccountData,
    AccountDelete,
    HomeView,
    LoginView,
    LogoutView,
    RegisterApi,
    UserView,
    deposit,
    transfer,
    UsersData,
    User,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/register/", RegisterApi.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/userview/", UserView.as_view(), name="userview"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/users/", UsersData.as_view(), name="users_data"),
    path("api/account/", AccountData.as_view(), name="account_data"),
    path("api/account-update/", AccountDelete.as_view(), name="account_delete"),
    path("api/user/<int:pk>/", User.as_view(), name="user"),
    # path("api/register/", register, name="register"),
    # path("api/login/", login, name="register"),
    path("api/deposit/", deposit, name="deposit"),
    path("api/transfer/", transfer, name="transfer"),
    path("api/users/", UsersData.as_view(), name="users_data"),
    path("api/user/<int:pk>/", User.as_view(), name="user"),
]
