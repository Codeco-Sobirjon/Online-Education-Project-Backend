# Generated by Django 5.0.4 on 2024-07-31 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_phone_number_alter_user_bio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, unique=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'config',
                'verbose_name_plural': 'configs',
                'db_table': 'configs',
                'ordering': ('key',),
            },
        ),
    ]
