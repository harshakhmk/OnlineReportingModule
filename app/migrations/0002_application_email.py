# Generated by Django 3.2.7 on 2021-09-19 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='email',
            field=models.EmailField(blank=True, db_index=True, default='example@example.com', max_length=254, null=True),
        ),
    ]
