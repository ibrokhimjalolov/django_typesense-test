# Generated by Django 4.1.7 on 2023-02-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='number',
            field=models.IntegerField(default=5),
        ),
    ]
