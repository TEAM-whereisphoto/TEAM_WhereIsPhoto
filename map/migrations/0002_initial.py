
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
        ('map', '0001_initial'),
        ('brand', '0001_initial'),

    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='liked',
            name='booth',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.booth'),
        ),
        migrations.AddField(
            model_name='liked',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='booth',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brand.brand'),
        ),
        migrations.AddField(
            model_name='booth',
            name='user',
            field=models.ManyToManyField(through='map.Liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
