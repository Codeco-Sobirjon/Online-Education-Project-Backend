# Generated by Django 5.0.4 on 2024-08-02 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]