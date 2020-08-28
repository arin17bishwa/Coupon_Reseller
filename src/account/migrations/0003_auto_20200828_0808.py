# Generated by Django 3.1 on 2020-08-28 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_userprofile_name_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='name_verified',
        ),
        migrations.AddField(
            model_name='user',
            name='name_verified',
            field=models.BooleanField(default=False),
        ),
    ]
