# Generated by Django 3.1.6 on 2021-02-18 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20210218_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipelist',
            name='amount',
            field=models.IntegerField(default=1),
        ),
    ]
