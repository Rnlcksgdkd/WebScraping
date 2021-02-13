# Generated by Django 3.1.5 on 2021-02-06 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomID', models.TextField()),
                ('room_name', models.TextField()),
                ('location', models.TextField()),
                ('latitude', models.TextField()),
                ('longitude', models.TextField()),
                ('link', models.URLField()),
                ('image_link', models.URLField()),
            ],
        ),
    ]
