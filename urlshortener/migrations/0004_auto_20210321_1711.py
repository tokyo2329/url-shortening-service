# Generated by Django 3.1.7 on 2021-03-21 17:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortener', '0003_auto_20210321_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='expires_after',
            field=models.DateField(default=datetime.datetime(2021, 3, 28, 17, 11, 6, 666415)),
        ),
    ]
