# Generated by Django 4.2.6 on 2023-11-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_bookmark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
        migrations.AddField(
            model_name='article',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
    ]
