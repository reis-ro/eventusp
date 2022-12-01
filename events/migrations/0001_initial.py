# Generated by Django 4.1.3 on 2022-12-01 00:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_promotor_profile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField(blank=True, null=True, verbose_name='data')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='tempo')),
                ('duration', models.TimeField(blank=True, null=True, verbose_name='duracao')),
                ('place', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1500)),
                ('summary', models.CharField(max_length=500)),
                ('max_participants', models.IntegerField()),
                ('cover_photo_url', models.URLField(null=True)),
                ('event_photo_url', models.URLField(null=True)),
                ('approved', models.BooleanField(default=False, verbose_name='Aprovado')),
                ('promotor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.promotor')),
            ],
        ),
        migrations.CreateModel(
            name='Formato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formato', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='TipoOrganizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_org', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('events', models.ManyToManyField(to='events.event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='formato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.formato'),
        ),
        migrations.AddField(
            model_name='event',
            name='tema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.tema'),
        ),
        migrations.AddField(
            model_name='event',
            name='tipo_organizacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.tipoorganizacao'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('likes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
    ]
