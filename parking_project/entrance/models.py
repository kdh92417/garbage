from django.db import models

class Car(models.Model):
    number        = models.IntegerField(max_length=100)
    type          = models.CharField(max_length= 100)
    start_date    = models.DateField(null=True)
    expire_date   = models.DateField(null=True)

    class Meta:
        db_table = 'cars'


class Record(models.Model):
    entry_time     = models.TimeField(auto_now_add=True)
    departure_time = models.TimeField(null=True)
    parking_time   = models.TimeField(null=True)
    car            = models.ForeignKey('Car', on_delete=models.CASCADE)

    class Meta:
        db_table = 'records'


class PaymentRecord(models.Model):
    paid_amount         = models.IntegerField(max_length=100)
    discount_amount     = models.IntegerField(max_length=100, null=True)
    total_paid_amount   = models.IntegerField(max_length=100, null=True)
    paid_time           = models.DateTimeField(auto_now_add=True, null=True)
    payment_success     = models.BooleanField(null=True)
    payment_method      = models.CharField(max_length=100, null=True)
    record              = models.ForeignKey('Record', on_delete=models.CASCADE)

    class Meta:
        db_table = 'payment_records'

