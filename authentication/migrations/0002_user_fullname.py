# Generated by Django 3.2.7 on 2021-09-19 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fullname',
            field=models.CharField(blank=True, default='username', max_length=255, null=True),
        ),
    ]
