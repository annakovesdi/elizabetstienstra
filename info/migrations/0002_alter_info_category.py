# Generated by Django 4.2.6 on 2023-11-08 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='info.category'),
        ),
    ]
