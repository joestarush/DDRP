# Generated by Django 5.0.7 on 2024-07-23 16:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0006_temp_log_qr"),
    ]

    operations = [
        migrations.AddField(
            model_name="temp_log_qr",
            name="phone_number",
            field=models.CharField(default=1, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
