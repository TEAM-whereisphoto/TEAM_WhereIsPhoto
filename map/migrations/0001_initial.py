# Generated by Django 4.0.2 on 2022-02-04 05:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.IntegerField()),
                ('location', models.TextField()),
                ('operationHour', models.TimeField()),
                ('brand', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('img', models.ImageField(blank=True, null=True, upload_to='')),
                ('rate', models.IntegerField()),
                ('booth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.booth')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Liked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('booth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.booth')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='booth',
            name='user',
            field=models.ManyToManyField(through='map.Liked', to=settings.AUTH_USER_MODEL),
        ),
    ]