# Generated by Django 3.0.5 on 2020-05-27 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodItems', '0004_auto_20200526_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='serviceable',
            field=models.CharField(choices=[('Available', 'Service Available'), ('Not Available', 'Service Not Available')], default='Service Available', max_length=30),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='veg',
            field=models.CharField(choices=[('Veg', 'Veg'), ('Non-veg', 'Non-Veg')], default='Veg', max_length=100),
        ),
    ]
