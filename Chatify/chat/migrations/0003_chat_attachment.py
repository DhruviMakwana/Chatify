# Generated by Django 4.2 on 2023-06-15 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_user_block_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="attachment",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
