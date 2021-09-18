# Generated by Django 3.2.7 on 2021-09-18 03:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], max_length=10)),
                ('reason', models.TextField()),
                ('message', models.TextField()),
                ('apply_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('DoB', models.DateField(auto_now=True)),
                ('Aadhar', models.CharField(max_length=16)),
                ('Passport', models.CharField(max_length=20)),
                ('Address', models.TextField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=20)),
                ('pwd_category', models.TextField(blank=True, max_length=255, null=True)),
                ('documents', models.FileField(upload_to='documents')),
                ('passport_pic', models.ImageField(upload_to='passport_pic')),
                ('Notes', models.TextField()),
                ('registration_no', models.IntegerField(blank=True, null=True, unique=True)),
                ('application_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.applicationstatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
