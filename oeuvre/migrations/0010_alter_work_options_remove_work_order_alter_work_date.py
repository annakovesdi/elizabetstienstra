# Generated by Django 4.2.6 on 2024-02-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oeuvre', '0009_remove_category_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='work',
            options={'ordering': ('-date',)},
        ),
        migrations.RemoveField(
            model_name='work',
            name='order',
        ),
        migrations.AlterField(
            model_name='work',
            name='date',
            field=models.DateField(verbose_name='date, format dd-mm-yyyy'),
        ),
    ]
