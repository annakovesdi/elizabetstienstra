# Generated by Django 4.2.6 on 2023-10-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oeuvre', '0002_remove_work_image_remove_work_image10_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='date',
            field=models.DateField(),
        ),
    ]
