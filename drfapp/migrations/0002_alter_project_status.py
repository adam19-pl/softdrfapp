# Generated by Django 4.0 on 2022-01-05 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[(0, 'new'), (1, 'old')], default=(0, 'new'), max_length=256),
        ),
    ]