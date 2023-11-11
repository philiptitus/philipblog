# Generated by Django 4.2.6 on 2023-11-06 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='swift.jpg', upload_to='articles/')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
        migrations.AddField(
            model_name='article',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='articles', to='articles.articleimage'),
        ),
    ]