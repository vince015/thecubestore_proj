import decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=True)

    merchant_id = models.CharField(primary_key=True,
                                   unique=True,
                                   max_length=64)
    remarks = models.CharField(max_length=256,
                               blank=True,
                               null=True)

class Contact(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=True)

    contact_number = models.CharField(max_length=18,
                                      blank=False,
                                      null=True)
    primary_address = models.CharField(max_length=2048,
                                       blank=True,
                                       null=True)
    alternate_address = models.CharField(max_length=2048,
                                         blank=True,
                                         null=True)

class Store(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=True)
    name = models.CharField(max_length=64,
                            blank=False,
                            null=True)
    product = models.CharField(max_length=128,
                               blank=True,
                               null=True)
    facebook = models.CharField(max_length=64,
                                blank=True,
                                null=True)
    instagram = models.CharField(max_length=64,
                                 blank=True,
                                 null=True)
    website = models.URLField(max_length=128,
                              blank=True,
                              null=True)

class Bank(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=True)
    owner = models.CharField(max_length=256,
                             blank=False,
                             null=True)
    bank = models.CharField(max_length=128,
                            blank=False,
                            null=True)
    account = models.CharField(max_length=128,
                               blank=False,
                               null=True)

class Cube(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=False,
                             null=True)
    unit = models.CharField(blank=False,
                            max_length=128,
                            null=True)
    rate = models.DecimalField(max_digits=7,
                               decimal_places=2,
                               null=True,
                               validators=[MinValueValidator(decimal.Decimal('0.01'))])
    duration = models.PositiveSmallIntegerField(blank=True,
                                                null=True)
    promo = models.PositiveSmallIntegerField(blank=True,
                                             default=0,
                                             null=True)
    start_date = models.DateField(blank=True,
                                  null=True)
    end_date = models.DateField(blank=True,
                                null=True)
    next_due_date = models.DateField(null=True,
                                     blank=True)
    remarks = models.CharField(max_length=256,
                               blank=True,
                               null=True)

class Item(models.Model):

    cube = models.ForeignKey(Cube,
                             on_delete=models.CASCADE,
                             blank=False,
                             null=True)
    code = models.CharField(max_length=64,
                            null=True,
                            unique=True)
    quantity = models.PositiveSmallIntegerField(blank=False,
                                                null=True)
    price = models.DecimalField(max_digits=7,
                                decimal_places=2,
                                null=True,
                                validators=[MinValueValidator(decimal.Decimal('0.01'))])
    vat = models.DecimalField(default=0,
                              max_digits=5,
                              decimal_places=2,
                              null=True)
    commission = models.DecimalField(default=0,
                                     max_digits=5,
                                     decimal_places=2,
                                     null=True)
    description = models.CharField(max_length=256,
                                   null=True)

class Payout(models.Model):

    merchant = models.ForeignKey(User,
                                 models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 default=0)
    bank = models.ForeignKey(Bank,
                             models.SET_NULL,
                             blank=True,
                             null=True,
                             default=0)
    reference_number = models.CharField(max_length=64,
                                        blank=False,
                                        null=True)
    date = models.DateField(blank=False)
    amount = models.DecimalField(blank=False,
                                 max_digits=7,
                                 decimal_places=2,
                                 null=True)
    remarks = models.CharField(max_length=256,
                               null=True,
                               blank=True)

class Sales(models.Model):

    item = models.CharField(max_length=64,
                            blank=False,
                            null=True)
    quantity = models.PositiveSmallIntegerField(blank=False,
                                                null=True)
    date = models.DateField(blank=False,
                            null=True)
    gross = models.DecimalField(max_digits=7,
                                decimal_places=2,
                                null=True)
    net = models.DecimalField(max_digits=7,
                              decimal_places=2,
                              null=True)
    payout = models.IntegerField(blank=True,
                                 null=True,
                                 default=0)

    class Meta:
         verbose_name = "Sale"

class Announcement(models.Model):

    issue_date = models.DateField(blank=False,
                                  null=True)
    subject = models.CharField(max_length=128,
                               blank=False,
                               null=True)
    detail = models.CharField(max_length=2048,
                              blank=False,
                              null=True)
