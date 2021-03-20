# Generated by Django 3.1.7 on 2021-03-09 20:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("urlshortener", "0007_auto_20210309_2007"),
    ]

    operations = [
        migrations.AddField(
            model_name="url",
            name="expires_after_x_clicks",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="url",
            name="expires_after",
            field=models.DateField(
                default=datetime.datetime(2021, 3, 16, 20, 9, 16, 541888)
            ),
        ),
    ]
