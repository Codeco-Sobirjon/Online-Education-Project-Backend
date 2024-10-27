# Generated by Django 5.0.4 on 2024-07-23 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='lessons_per_part',
        ),
        migrations.RemoveField(
            model_name='course',
            name='price_per_lesson',
        ),
        migrations.AddField(
            model_name='course',
            name='discounted_lesson_price',
            field=models.PositiveIntegerField(null=True, verbose_name='discounted lesson price'),
        ),
        migrations.AddField(
            model_name='course',
            name='lesson_price',
            field=models.PositiveIntegerField(default=15, verbose_name='lesson price'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='part_lesson_count',
            field=models.PositiveIntegerField(default=10, verbose_name='part lesson count'),
        ),
    ]