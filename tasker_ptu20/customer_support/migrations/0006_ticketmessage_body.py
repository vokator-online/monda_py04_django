# Generated by Django 5.0 on 2024-03-21 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_support', '0005_alter_ticketmessage_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketmessage',
            name='body',
            field=models.TextField(blank=True, default='', max_length=10000, verbose_name='body'),
        ),
    ]