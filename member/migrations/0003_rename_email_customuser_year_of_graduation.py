# Generated by Django 4.2.15 on 2024-09-21 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("member", "0002_customuser_email_customuser_interest_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="email",
            new_name="year_of_graduation",
        ),
    ]
