# Generated by Django 5.0.4 on 2024-07-22 11:28

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'category',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='name')),
                ('hex_code', models.CharField(max_length=7, unique=True, verbose_name='hex code')),
            ],
            options={
                'verbose_name': 'color',
                'verbose_name_plural': 'colors',
                'db_table': 'color',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('order', models.SmallIntegerField(blank=True, verbose_name='order')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
                'db_table': 'section',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('video_1080p', models.URLField(blank=True, null=True, verbose_name='1080p Video')),
                ('video_720p', models.URLField(verbose_name='720p Video')),
                ('video_480p', models.URLField(verbose_name='480p Video')),
                ('video_360p', models.URLField(verbose_name='360p Video')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
                'db_table': 'video',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='CompletedLesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('completed_at', models.DateTimeField(auto_now_add=True, verbose_name='completed at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completed_lessons', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'completed lesson',
                'verbose_name_plural': 'completed lessons',
                'db_table': 'completed_lesson',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('is_fragment', models.BooleanField(default=False, verbose_name='is fragment')),
                ('image', models.ImageField(upload_to='course-images/')),
                ('video', models.FileField(upload_to='course-videos/')),
                ('lessons_per_part', models.PositiveSmallIntegerField(default=10, verbose_name='Lessons per Part')),
                ('price_per_lesson', models.PositiveIntegerField(default=0, verbose_name='price per lesson')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='course.category', verbose_name='category')),
                ('color1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_in_1st', to='course.color', verbose_name='1st color')),
                ('color2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_in_2st', to='course.color', verbose_name='2nd color')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL, verbose_name='teacher')),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
                'db_table': 'course',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CoursePart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order', models.PositiveSmallIntegerField(blank=True, verbose_name='order')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='course.course')),
            ],
            options={
                'verbose_name': 'course part',
                'verbose_name_plural': 'course parts',
                'db_table': 'course_part',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created at')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='course.course', verbose_name='course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'enrollment',
                'verbose_name_plural': 'enrollments',
                'db_table': 'enrollment',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('duration', models.PositiveSmallIntegerField()),
                ('order', models.SmallIntegerField(blank=True, verbose_name='order')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created at')),
                ('part', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='course.coursepart')),
            ],
            options={
                'verbose_name': 'lesson',
                'verbose_name_plural': 'lessons',
                'db_table': 'lesson',
                'ordering': ['order'],
            },
        ),
    ]
