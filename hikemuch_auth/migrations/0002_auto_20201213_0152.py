# Generated by Django 3.1.4 on 2020-12-12 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hikemuch_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateTimeField(blank=True),
        ),
    ]