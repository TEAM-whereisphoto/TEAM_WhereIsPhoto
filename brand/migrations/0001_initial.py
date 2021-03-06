
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('retake', models.CharField(max_length=50)),
                ('remote', models.CharField(max_length=50)),
                ('QR', models.CharField(max_length=50)),
                ('etc', models.TextField(null=True)),
                ('time', models.CharField(max_length=50)),
                ('img', models.ImageField(upload_to='')),
                ('liked_img', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('frame', models.CharField(max_length=50)),
                ('take', models.IntegerField()),
                ('price', models.IntegerField()),
                ('etc', models.CharField(max_length=200, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
            ],
        ),
    ]
