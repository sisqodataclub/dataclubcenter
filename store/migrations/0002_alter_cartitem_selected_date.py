# Generated by Django 5.0.4 on 2024-04-11 02:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="selected_date",
            field=models.CharField(blank=True, default="", max_length=1000),
        ),
    ]