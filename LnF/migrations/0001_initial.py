# Generated by Django 4.0.2 on 2022-02-20 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('read', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LnF_Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='LnF')),
                ('content', models.TextField()),
                ('tag', models.CharField(choices=[('분실', '분실'), ('보관', '보관')], max_length=50)),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
