# Generated by Django 5.1.2 on 2024-10-29 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("web_app", "0003_alter_user_is_superuser"),
    ]

    operations = [
        migrations.DeleteModel(
            name="User",
        ),
    ]
