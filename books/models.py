from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Link to the book
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the book
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when added

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in {self.user.username}'s cart"

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)  # Link to the User model
#     wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # User's wallet balance

#     def __str__(self):
#         return f"{self.user.username}'s Profile"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)  # Ensure uniqueness
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Profile"