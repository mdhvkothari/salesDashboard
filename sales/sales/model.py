# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TotalSalesData(models.Model):
    id = models.BigIntegerField(db_column='Id', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    sales_channel = models.TextField(db_column='Sales Channel', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sales_order_id = models.TextField(db_column='Sales order ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ship_to_name = models.TextField(db_column='Ship to name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sku = models.TextField(db_column='SKU', blank=True, null=True)  # Field name made lowercase.
    normal_sku = models.TextField(db_column='Normal SKU', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    vendor = models.TextField(db_column='Vendor', blank=True, null=True)  # Field name made lowercase.
    quantity = models.FloatField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    line_total = models.FloatField(db_column='Line Total', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    channel_order_id = models.TextField(db_column='channel order id', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    vendor_type = models.TextField(db_column='Vendor type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'total_sales_data'

class TotalOpalData(models.Model):
    id = models.BigIntegerField(db_column='Id', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    orderdate = models.DateField(db_column='orderDate', blank=True, null=True)  # Field name made lowercase.
    orderid = models.FloatField(db_column='orderId', blank=True, null=True)  # Field name made lowercase.
    customerreferencenumber = models.TextField(db_column='customerReferenceNumber', blank=True, null=True)  # Field name made lowercase.
    invoicenumber = models.FloatField(db_column='invoiceNumber', blank=True, null=True)  # Field name made lowercase.
    itemname = models.TextField(db_column='itemName', blank=True, null=True)  # Field name made lowercase.
    quantity = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    customername = models.TextField(db_column='customerName', blank=True, null=True)  # Field name made lowercase.
    orderstatus = models.TextField(db_column='orderStatus', blank=True, null=True)  # Field name made lowercase.
    shippingcarrier = models.TextField(db_column='shippingCarrier', blank=True, null=True)  # Field name made lowercase.
    vendor = models.TextField(db_column='Vendor', blank=True, null=True)  # Field name made lowercase.
    vendortype = models.TextField(db_column='vendorType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'total_opal_data'