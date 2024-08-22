from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import AbstractUser
from ecommerce.settings import AUTH_USER_MODEL


class User(AbstractUser):
    pass


# # Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=200)
#     date_added = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-date_added']
#     def __str__(self):
#         return self.name    
    
    

    
class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.CharField(max_length=5000, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=0)
    class Meta:
        ordering = ['-date_added']  

    def __str__(self):
        return self.title  


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    
    
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

   
# class Commande(models.Model):
#     items = models.CharField(max_length=300)
#     total = models.CharField(max_length=200)
#     nom = models.CharField(max_length=150)
#     email = models.EmailField()
#     address = models.CharField(max_length=200)
#     ville = models.CharField(max_length=200)
#     pays = models.CharField(max_length=300)
#     zipcode = models.CharField(max_length=300)
#     date_commande = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-date_commande']

#     def __str__(self):
#         return self.nom   