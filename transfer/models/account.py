from django.db import models
from transfer.models.user_model import CustomUser

class Account(models.Model):
    """Represents paynow Account"""
    client = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
