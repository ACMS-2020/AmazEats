# Generated by Django 3.0.5 on 2020-05-22 09:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0008_auto_20200522_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 22, 14, 52, 24, 728016)),
        ),
    ]
