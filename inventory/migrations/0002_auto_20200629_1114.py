# Generated by Django 3.0.7 on 2020-06-29 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='init_qty',
            field=models.IntegerField(),
        ),
    ]
