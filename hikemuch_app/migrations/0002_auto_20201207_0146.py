# Generated by Django 3.1.4 on 2020-12-06 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hikemuch_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='hikes')),
            ],
        ),
        migrations.DeleteModel(
            name='Python',
        ),
    ]