# Generated by Django 3.1 on 2020-08-14 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_customer',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_business_owner',
            field=models.BooleanField(default=False),
        ),
    ]