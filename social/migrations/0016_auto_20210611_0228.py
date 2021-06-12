# Generated by Django 3.2.4 on 2021-06-11 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0015_auto_20210611_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='social.Image'),
        ),
    ]
