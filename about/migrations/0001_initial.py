# Generated by Django 4.2.6 on 2023-10-26 11:42

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254)),
                ('description', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(upload_to='')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='')),
                ('contact', models.CharField(max_length=100)),
            ],
        ),
    ]
