# Generated by Django 3.1.6 on 2021-02-21 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=20),
        ),
    ]