from django.contrib import admin
from transfer.models.account import Account
from transfer.models.deposit_model import Deposit
from transfer.models.transaction import Transaction

# Register your models here.

from transfer.models.user_model import CustomUser

admin.site.register(CustomUser)
admin.site.register(Deposit)
admin.site.register(Transaction)
admin.site.register(Account)
