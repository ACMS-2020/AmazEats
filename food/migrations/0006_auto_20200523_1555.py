# Generated by Django 3.0.5 on 2020-05-23 10:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_auto_20200520_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 23, 15, 55, 54, 762595)),
        ),
    ]