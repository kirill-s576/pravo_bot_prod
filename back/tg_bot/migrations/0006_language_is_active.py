# Generated by Django 3.1.7 on 2021-05-02 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0005_auto_20210402_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
