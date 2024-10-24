from typing import Any
from django.db import models

# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    message= models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return self.name



class User(models.Model):
    name= models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    password = models.CharField(max_length=20,null=True,blank=True)
    otp=models.IntegerField(default=0,null=True,blank=True)
    def __str__(self) -> str:
        return self.name
    

class Categories(models.Model):
    name=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self) -> str:
        return self.name
    

class Price(models.Model):
    name=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self) -> str:
        return self.name
    
class Additional(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self) -> str:
        return self.name    

  

class Product(models.Model):
    cat_id = models.ForeignKey(Categories,on_delete=models.CASCADE,blank=True,null=True)
    price_id = models.ForeignKey(Price,on_delete=models.CASCADE,blank=True,null=True)
    Additional_filter = models.ForeignKey(Additional,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50,null=True,blank=True) 
    image = models.ImageField(upload_to="media",null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True) 
    desciption = models.TextField(null=True,blank=True) 
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.name
       
class Add_to_cart(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50,null=True,blank=True) 
    image = models.ImageField(upload_to="media",null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True) 
    price = models.IntegerField()
    total_price = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    
class Add_to_Wishlist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50,null=True,blank=True) 
    image = models.ImageField(upload_to="media",null=True,blank=True)
    price = models.IntegerField()
     
    def __str__(self) -> str:
        return self.name 
    

    

class Coupon(models.Model):
    code=models.CharField(max_length=40,blank=True,null=True)
    discount=models.IntegerField(default=0,blank=True,null=True)  
    one_time_use=models.BooleanField(default=False)
    expiry_date=models.DateTimeField(blank=True,null=True)

    
    def __str__(self):
        return self.code