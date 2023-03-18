# Generated by Django 4.1.7 on 2023-03-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stockdata",
            name="close",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="stockdata",
            name="high",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="stockdata",
            name="low",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="stockdata",
            name="open",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="stockdata",
            name="vwap",
            field=models.CharField(max_length=10),
        ),
    ]
