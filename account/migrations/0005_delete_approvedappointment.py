# Generated by Django 4.1.3 on 2023-01-08 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_approvedappointment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApprovedAppointment',
        ),
    ]
