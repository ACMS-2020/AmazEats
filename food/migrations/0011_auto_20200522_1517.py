# Generated by Django 3.0.5 on 2020-05-22 09:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20200522_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 22, 15, 17, 52, 937378)),
        ),
    ]
