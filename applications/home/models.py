from django.db import models

# Create your models here.

class Donativo(models.Model):
    email = models.EmailField(max_length=254)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donativo de {self.email} - {self.amount} €"