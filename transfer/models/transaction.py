from django.db import models

from transfer.models.user_model import CustomUser


class Transaction(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sender"
    )
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="recipient"
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
