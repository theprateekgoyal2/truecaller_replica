# Generated by Django 4.2.7 on 2023-11-12 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contacts', '0002_rename_mapusercontact_usermapcontact'),
    ]

    operations = [
        migrations.CreateModel(
            name='spamPhoneNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField(unique=True)),
                ('spam', models.BooleanField(default=False)),
            ],
        ),
    ]
