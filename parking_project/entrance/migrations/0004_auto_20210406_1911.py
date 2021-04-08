# Generated by Django 3.0.7 on 2021-04-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrance', '0003_auto_20210406_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='departure_time',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='entry_time',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='parking_time',
            field=models.DateField(null=True),
        ),
    ]