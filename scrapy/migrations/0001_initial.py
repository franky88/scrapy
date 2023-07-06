# Generated by Django 4.2.2 on 2023-07-06 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True, null=True, verbose_name='links')),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='URLaddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'URL addresses',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('link', models.URLField()),
                ('disclosure', models.CharField(blank=True, max_length=120, null=True, verbose_name='disclosure')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapy.page')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='url_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapy.urladdress'),
        ),
    ]