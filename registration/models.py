# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Farmers(models.Model):
    first_name = models.CharField(max_length=255, )
    last_name = models.CharField(max_length=255)
    other_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)
    language = models.CharField(max_length=255, default='English')
    district = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    crop = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self, ):
        return self.phone_number


class SeedBag(models.Model):
    farmer = models.ForeignKey(Farmers, on_delete=models.CASCADE)
    bag_unique_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self, ):
        return self.bag_unique_number
