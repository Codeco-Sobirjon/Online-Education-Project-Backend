# Generated by Django 5.0.4 on 2024-07-25 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='image',
            field=models.ImageField(null=True, upload_to='notification/'),
        ),
    ]
