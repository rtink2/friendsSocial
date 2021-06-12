# Generated by Django 3.2.4 on 2021-06-09 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0012_messagemodel_threadmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='social.threadmodel'),
        ),
    ]
