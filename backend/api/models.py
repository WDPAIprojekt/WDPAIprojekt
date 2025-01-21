# from django.db import models
# from django.contrib.auth.models import AbstractUser, Group, Permission

# class SystemUser(AbstractUser):
#     """
#     Systemowy użytkownik odpowiedzialny za logowanie i rejestrację.
#     """
#     email=models.EmailField(blank=True, null=True)

#     groups = models.ManyToManyField(
#         Group,
#         related_name="custom_user_set", 
#         blank=True,
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name="custom_user_permissions_set",  
#         blank=True,
#     )

# class Budget(models.Model):
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Expense(models.Model):
#     budget = models.ForeignKey(Budget, related_name='expenses', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class SystemUser(AbstractUser):
    """
    Systemowy użytkownik odpowiedzialny za logowanie i rejestrację.
    """
    email = models.EmailField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set", 
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  
        blank=True,
    )

    def __str__(self):
        # Zwraca czytelną reprezentację użytkownika
        return f"{self.username}"

class Budget(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(SystemUser, related_name='user', on_delete=models.CASCADE, null=True)

    def __str__(self):
        # Zwraca kwotę budżetu jako string
        return f"Budget: {self.total_amount} (created at {self.created_at.strftime('%Y-%m-%d')})"

class Expense(models.Model):
    budget = models.ForeignKey(Budget, related_name='expenses', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # Zwraca nazwę wydatku i jego kwotę
        return f"{self.name}: {self.amount} (Budget ID: {self.budget.id})"
