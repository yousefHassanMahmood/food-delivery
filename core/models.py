from django.db import models
import re

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        )
        # first name
        if not postData.get('first_name'):
            errors["missing_field_first_name"] = "Please enter first name."
        elif len(postData['first_name']) < 2:
            errors["first_name_length"] = "First Name should be at least 2 characters."

        # last name
        if not postData.get('last_name'):
            errors["missing_field_last_name"] = "Please enter last name."
        elif len(postData['last_name']) < 2:
            errors["last_name_length"] = "Last Name should be at least 2 characters."

        # email
        email = postData.get('email', '').strip()
        if not email:
            errors["missing_field_email"] = "Please enter an email."
        elif not EMAIL_REGEX.match(email):
            errors['email_format'] = "Invalid email address!"
        elif self.filter(email=email).exists():
            errors['email_taken'] = "That email is already registered."
        # address
        if not postData.get('address'):
            errors["missing_field_address"] = "Please enter address."
        elif len(postData['address']) < 2:
            errors["last_name_length"] = "address should be at least 2 characters."        

        # password + confirm
        pwd = postData.get('password','')
        cpwd = postData.get('confirm_pw','')
        if not (pwd and cpwd):
            errors["missing_field_password"] = "Please enter and confirm your password."
        elif len(pwd) < 8:
            errors["password_length"] = "Password should be at least 8 characters."
        elif pwd != cpwd:
            errors["password_confirm"] = "Passwords do not match."

        return errors

    def login_validator(self, postData):
        # you can flesh this out if you use it
        errors = {}
        if not postData.get('email') or not postData.get('password'):
            errors["login"] = "Invalid email or password."
        return errors


class User(models.Model):
    CUSTOMER   = 1
    RESTAURANT = 2
    USER_TYPE_CHOICES = (
        (CUSTOMER,   'Customer'),
        (RESTAURANT, 'Restaurant'),
    )

    first_name  = models.CharField(max_length=30)
    last_name   = models.CharField(max_length=30)
    email       = models.EmailField(max_length=60, unique=True)
    password    = models.CharField(max_length=128)
    address     = models.CharField(max_length=255, blank=True)
    phone       = models.CharField(max_length=20, blank=True)

    user_type   = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,
        default=CUSTOMER,
        help_text="1 = Customer, 2 = Restaurant"
    )

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    objects = UserManager()



class Restaurant(models.Model):
    owner       = models.ForeignKey(
                    User,
                    related_name='restaurants',
                    on_delete=models.CASCADE
                  )
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address     = models.CharField(max_length=255, blank=True)
    phone       = models.CharField(max_length=20, blank=True)
    avg_rating  = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class MenuItem(models.Model):
    restaurant  = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    image_url   = models.URLField(max_length=500, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)



class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending',       'Pending'),
        ('Preparing',     'Preparing'),
        ('OutForDelivery','Out for Delivery'),
        ('Delivered',     'Delivered'),
        ('Cancelled',     'Cancelled'),
    ]

    user= models.ForeignKey(User,
  related_name='orders',
  on_delete=models.CASCADE)
    restaurant       = models.ForeignKey(Restaurant,
  related_name='orders',
  on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    total_price      = models.DecimalField(max_digits=10, decimal_places=2)
    status           = models.CharField(max_length=20,
 choices=STATUS_CHOICES,
 default='Pending')
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)




class OrderItem(models.Model):
    order      = models.ForeignKey(Order,    related_name='items', on_delete=models.CASCADE)
    menu_item  = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity   = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)




class Review(models.Model):
    user        = models.ForeignKey(User,
          related_name='reviews',
          on_delete=models.CASCADE)
    restaurant  = models.ForeignKey(Restaurant,
          related_name='reviews',
          on_delete=models.CASCADE)
    rating      = models.PositiveSmallIntegerField()
    comment     = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


