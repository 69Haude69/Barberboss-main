from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length =100)
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ('barber', 'Barber'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]
    phone = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    full_name = models.CharField(max_length= 300)
    bio= models.CharField(max_length = 300)
    image = models.ImageField(default = "default.jpg", upload_to="user_images")
    verified = models.BooleanField(default = False)
    def __str__(self):
        return self.full_name
    
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile,sender=User)

class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='barber')

User = get_user_model()

class Barbershop(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    address = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Check if the barbershop is being created for the first time
        if not self.pk:
            # Create default styles of cut for the new barbershop
            StyleOfCut.create_default_styles(self)

class StyleOfCut(models.Model):
    DEFAULT_STYLES = [
        {'name': 'Hait Cut', 'price': 200},
        {'name': 'Designed Hair Cut', 'price': 350},
        {'name': 'Beard Cut', 'price': 120},
        {'name': 'Beard Trimming', 'price': 150},
        {'name': 'Head Massage ', 'price': 200},
        {'name': 'Hair Shampoo', 'price': 120},
        {'name': 'Face Bleech', 'price': 700},
        {'name': 'Facial', 'price': 1000},
        {'name': 'Face Wash', 'price': 400},
        {'name': 'Hair Color Black', 'price': 500},
        {'name': 'Threading', 'price': 120},
        {'name': 'Hair Highlight', 'price': 1000},
        {'name': 'Straightining Hair', 'price': 1800},
        {'name': 'Hair Iron', 'price': 700},
        {'name': 'Hair Treatment', 'price': 650},
        {'name': 'Hair Deadlock', 'price': 12000},
        {'name': 'Hair Curl', 'price': 3500},
        {'name': 'Hair Threading', 'price': 1800},

    ]
    
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name='styles_of_cut')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @classmethod
    def create_default_styles(cls, barbershop):
        for default_style in cls.DEFAULT_STYLES:
            cls.objects.create(barbershop=barbershop, **default_style)


class Appointment(models.Model):
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name='appointments')
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='appointments')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    style_of_cut = models.ForeignKey(StyleOfCut, on_delete=models.CASCADE, related_name='appointments')
    date_time = models.DateTimeField()
