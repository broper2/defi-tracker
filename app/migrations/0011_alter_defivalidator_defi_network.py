# Generated by Django 4.0 on 2021-12-20 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_defivalidator_defi_network'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defivalidator',
            name='defi_network',
            field=models.CharField(default='solana', max_length=50),
        ),
    ]
