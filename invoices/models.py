from django.db import models

# Create your models here.
class Invoice(models.Model):
    #userid=models.CharField(max_length=100)
    userid=models.PositiveIntegerField(null=True)
    invoicedata=models.DateTimeField(auto_now=True)
    itemid=models.PositiveIntegerField(null=True)
    unitprice=models.DecimalField(max_digits=8, decimal_places=2)
    quantity=models.DecimalField(max_digits=8, decimal_places=2)
    invoicetotal=models.DecimalField(max_digits=8, decimal_places=2)