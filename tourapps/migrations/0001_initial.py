# Generated by Django 4.0.6 on 2022-07-20 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banner')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('age_range', models.IntegerField()),
                ('price', models.IntegerField()),
                ('main_photo', models.ImageField(upload_to='photos')),
                ('photo_1', models.ImageField(upload_to='photos')),
                ('photo_2', models.ImageField(upload_to='photos')),
                ('photo_3', models.ImageField(upload_to='photos')),
                ('refund_policy', models.CharField(max_length=200)),
                ('package', models.CharField(choices=[('Air fares', 'Air fares'), ('4 Nights Hotel Accomodation', '4 Nights Hotel Accomodation'), ('Entrance Fees', 'Entrance Fees'), ('Tour Guide', 'Tour Guide')], max_length=200)),
                ('departure', models.DateTimeField(default=datetime.datetime.now)),
                ('arrival', models.DateTimeField(default=datetime.datetime.now)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]