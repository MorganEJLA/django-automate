# Generated by Django 5.0.3 on 2024-03-13 00:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dataentry", "0002_dessert_featured_ingredient"),
    ]

    operations = [
        migrations.AddField(
            model_name="dessert",
            name="additional_ingredient",
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
    ]
