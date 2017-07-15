from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Contact(models.Model):

    # Validator for phone number
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,13}$',
                                 message="Phone number must be entered in the format:\
                                          '+63xxxxxxxxxx'. Up to 13 digits allowed.")

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=True)

    contact_number = models.CharField(max_length=13,
                                      validators=[phone_regex],
                                      blank=False)
    primary_address = models.CharField(max_length=2048,
                                       blank=True)
    alternate_address = models.CharField(max_length=2048,
                                         blank=True)

class Store(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=True)
    name = models.CharField(max_length=64,
                            blank=False)
    product = models.CharField(max_length=128,
                               blank=True,
                               null=True)
    facebook = models.CharField(max_length=64,
                                blank=True,
                                null=True)
    instagram = models.CharField(max_length=64,
                                 blank=True,
                                 null=True)
    website = models.CharField(max_length=128,
                               blank=True,
                               null=True)

class Bank(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=True)
    owner = models.CharField(max_length=256,
                             blank=False)
    bank = models.CharField(max_length=128,
                            blank=False)
    account = models.CharField(max_length=128,
                               blank=False)