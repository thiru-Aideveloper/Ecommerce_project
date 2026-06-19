from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    price = models.IntegerField()

    description = models.TextField()

    image = models.ImageField(
        upload_to='products/'
    )

    def __str__(self):
        return self.name


# class Order(models.Model):

#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )

#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE
#     )

#     quantity = models.IntegerField(
#         default=1
#     )

#     amount = models.IntegerField()

#     payment_id = models.CharField(
#         max_length=200,
#         blank=True,
#         null=True
#     )

#     status = models.CharField(
#         max_length=50,
#         default='Pending'
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     def __str__(self):
#         return self.user.username
    


class Order(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    amount = models.IntegerField()

    payment_id = models.CharField(max_length=200)

    status = models.CharField(max_length=50,default="Paid")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username