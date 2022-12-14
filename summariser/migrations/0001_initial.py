# Generated by Django 4.1.4 on 2022-12-08 15:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to='audios/')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_speakers', models.IntegerField(blank=True, null=True)),
                ('transcript', models.TextField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('model', models.FileField(upload_to='models/')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
