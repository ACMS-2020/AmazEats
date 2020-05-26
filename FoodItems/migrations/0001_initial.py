# Generated by Django 3.0.6 on 2020-05-25 08:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('food_id', models.AutoField(primary_key=True, serialize=False)),
                ('food_name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('item_type', models.CharField(choices=[('Starters', 'Starters'), ('Main Courses', 'Main Course'), ('Desserts', 'Desserts'), ('Beverages', 'Beverages')], max_length=50, null=True)),
                ('serviceable', models.CharField(choices=[('available', 'service available'), ('not available', 'service not available')], default='service available', max_length=30)),
                ('veg', models.CharField(choices=[('veg', 'veg'), ('non-veg', 'non-veg')], default='veg', max_length=100)),
                ('cuisine_type', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery/')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Ustats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=220)),
                ('restaurant_rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('food_item', models.CharField(default='item ordered', max_length=220)),
                ('food_rating', models.PositiveIntegerField(default='1', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], default='month of ordering', max_length=10)),
                ('order_placed', models.PositiveIntegerField(default='1', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1)])),
                ('date_of_ordering', models.DateTimeField(blank=True, null=True)),
                ('money_spent', models.PositiveIntegerField(default='1', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5000)])),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
            ],
        ),
        migrations.CreateModel(
            name='Rstats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220)),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], default='month of ordering', max_length=10)),
                ('order_placed', models.PositiveIntegerField(default='1', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('money_spent', models.PositiveIntegerField(default='1', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5000)])),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.User')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('rating', models.IntegerField(default=0, null=True)),
                ('reviews', models.TextField(max_length=400, null=True)),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FoodItems.FoodItem')),
            ],
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_id', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=30)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Customer')),
            ],
        ),
    ]
