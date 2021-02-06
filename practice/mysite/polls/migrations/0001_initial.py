# Generated by Django 3.1.5 on 2021-02-02 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='host_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=50)),
                ('host_href', models.CharField(max_length=100)),
                ('host_rating', models.IntegerField(default=0)),
                ('host_num_rating', models.IntegerField(default=0)),
                ('host_region', models.CharField(max_length=50)),
            ],
        ),
    ]