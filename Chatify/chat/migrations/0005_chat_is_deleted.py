# Generated by Django 4.2 on 2023-06-19 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0004_alter_chat_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="is_deleted",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
