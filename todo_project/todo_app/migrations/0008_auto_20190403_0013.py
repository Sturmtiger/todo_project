# Generated by Django 2.1.7 on 2019-04-02 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0007_auto_20190403_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='colour',
            field=models.CharField(max_length=7, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
