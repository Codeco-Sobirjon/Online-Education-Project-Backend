# Generated by Django 5.0.4 on 2024-07-31 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_faqcategory_alter_config_id_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='faqcategory',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]