# Generated by Django 2.2.13 on 2022-01-31 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20220131_0551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'MALE'), ('female', 'FEMALE'), ('hermaphrodite', 'HERMAPHRODITE'), ('n/a', 'NA')], max_length=64),
        ),
    ]