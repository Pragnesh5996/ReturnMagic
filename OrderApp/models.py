from django.db import models

# Create your models here.
class installer(models.Model):
    hmac = models.CharField(max_length=2000)
    shop = models.CharField(max_length=2000)
    code = models.CharField(max_length=2000, default="")
    access_token = models.CharField(max_length=2000, default="")

class contact_details(models.Model):
    shopname = models.CharField(max_length=100)
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    subject_data = models.CharField(max_length=300)
    message_data = models.CharField(max_length=500)

class Homedata(models.Model):
    Desctiption = models.CharField(max_length=5000)

class about_data(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)

class Policy_data(models.Model):
    policy_title = models.CharField(max_length=1000)
    policy_description = models.CharField(max_length=5000)

class detail_order(models.Model):
    shop_data = models.CharField(max_length=1000)
    variants = models.CharField(max_length=5000)
    quantity = models.CharField(max_length=1000)
    order_id = models.CharField(max_length=1000)
    ordid = models.CharField(max_length=100)
    order_fulfill_status = models.CharField(max_length=500)
    order_total = models.CharField(max_length=500)
    status = models.CharField(max_length=1000)
    order_reason = models.TextField(max_length=2500, blank=True)
    order_note = models.TextField(max_length=2500, blank=True)
    crea_date = models.CharField(max_length=500, null=True)
    upda_date = models.CharField(max_length=500, null=True)
    tquant = models.CharField(max_length=20, default='')
    custom_id = models.CharField(max_length=20, default='')

class uninstall_data(models.Model):
    uninstall_shop = models.CharField(max_length=500)
    uninstall_time = models.CharField(max_length=200)