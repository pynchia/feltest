# Generated by Django 3.0.7 on 2020-06-30 09:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='supplier',
            field=models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
        migrations.AlterField(
            model_name='batch',
            name='tot_cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]