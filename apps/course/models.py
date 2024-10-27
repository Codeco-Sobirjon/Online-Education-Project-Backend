import decimal
import uuid

from django.db import models
from django.db.models import Avg, Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.accounts.models import User
from apps.course.utils import parting_course, reordering_sections, reordering_lessons


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='name')

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = 'name',

    @property
    def courses_count(self) -> int:
        return self.courses.count()


class Color(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, verbose_name='name', unique=True)
    hex_code = models.CharField(max_length=7, verbose_name='hex code', unique=True)

    class Meta:
        db_table = 'color'
        verbose_name = 'color'
        verbose_name_plural = 'colors'
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='courses', verbose_name="teacher", db_index=True)
    
    title = models.CharField(max_length=100, verbose_name="title", db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='courses', verbose_name="category", db_index=True)
    description = models.TextField(verbose_name="description")
    is_fragment = models.BooleanField(default=False, verbose_name="is fragment")
    image = models.ImageField(upload_to='course-images/')
    video = models.FileField(upload_to='course-videos/')
    color1 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='courses_in_1st', verbose_name='1st color')
    color2 = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='courses_in_2st', verbose_name='2nd color')
    part_lesson_count = models.PositiveIntegerField(verbose_name="part lesson count", default=10)
    lesson_price = models.PositiveIntegerField(verbose_name="lesson price", null=True)
    discounted_lesson_price = models.PositiveIntegerField(verbose_name="discounted lesson price", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")

    class Meta:
        db_table = 'course'
        verbose_name = 'course'
        verbose_name_plural = 'courses'
        ordering = ['-created_at']

    @property
    def lesson_count(self) -> int:
        return Lesson.objects.filter(section__course=self).count()
    
    @property
    def student_count(self) -> int:
        return self.enrollments.count()
    
    @property
    def review_count(self) -> int:
        return self.reviews.count()

    @property
    def average_rating(self) -> decimal.Decimal:
        rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return decimal.Decimal(round(rating, 1)) if rating else None
    
    @property
    def duration(self) -> int:
        course_duration = Lesson.objects.filter(section__course=self).aggregate(
            total_duration=Sum('duration')
        )['total_duration']
        return course_duration if course_duration else 0
    
    @property
    def price(self) -> int:
        return self.lesson_price * self.lesson_count

    @property
    def discounted_price(self) -> int:
        if self.discounted_lesson_price:
            return self.discounted_lesson_price * self.lesson_count
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        lessons = Lesson.objects.filter(section__course=self)
        parting_course(self, lessons)
        return super().save(*args, **kwargs)


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, verbose_name="title")
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='sections', verbose_name="course", db_index=True)
    order = models.SmallIntegerField(blank=True, verbose_name='order')

    class Meta:
        db_table = 'section'
        verbose_name = 'section'
        verbose_name_plural = 'sections'
        ordering = 'order',

    @property
    def lesson_count(self) -> int:
        return self.lessons.count()

    @property
    def duration(self) -> int:
        section_duration = self.lessons.all().aggregate(
            total_duration=Sum('duration')
        )['total_duration']
        return section_duration if section_duration else 0
    
    @property
    def price(self) -> int:
        return self.course.lesson_price * self.lesson_count

    @property
    def discounted_price(self) -> int:
        if self.course.discounted_lesson_price:
            return self.course.discounted_lesson_price * self.lesson_count
        return None

    def save(self, *args, **kwargs):
        course_sections = self.course.sections.all()
        if not self.order:
            self.order = course_sections.count() + 1
        return super().save(*args, **kwargs)


@receiver(post_save, sender=Section)
@receiver(post_delete, sender=Section)
def section_signal(sender, instance, **kwargs):
    course_sections = instance.course.sections.all().order_by('order')
    reordering_sections(course_sections)


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                related_name='lessons', verbose_name="section", db_index=True)
    part = models.ForeignKey('course.CoursePart', on_delete=models.CASCADE,
                             related_name='lessons', null=True, db_index=True)
    title = models.CharField(max_length=100, verbose_name="title")
    content = models.TextField(verbose_name="content")
    duration = models.PositiveSmallIntegerField()
    order = models.SmallIntegerField(blank=True, verbose_name='order')
    quiz_group = models.ForeignKey('quiz.QuizGroup', on_delete=models.CASCADE, db_index=True)
    is_open = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'lesson'
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'
        ordering = 'order',

    def save(self, *args, **kwargs):
        course_lessons = Lesson.objects.filter(section__course=self.section.course)
        if not self.order:
            self.order = course_lessons.count() + 1
        super().save(*args, **kwargs)
        lessons = Lesson.objects.filter(section__course=self.section.course)
        parting_course(self.section.course, lessons)
    

@receiver(post_save, sender=Lesson)
@receiver(post_delete, sender=Lesson)
def lesson_signal(sender, instance, **kwargs):
    course_lessons = Lesson.objects.filter(section__course=instance.section.course).order_by('section__order', 'order')
    reordering_lessons(course_lessons)


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='video', verbose_name="lesson")

    video_1080p = models.URLField(verbose_name="1080p Video", blank=True, null=True)
    video_720p = models.URLField(verbose_name="720p Video")
    video_480p = models.URLField(verbose_name="480p Video")
    video_360p = models.URLField(verbose_name="360p Video")

    created_at = models.DateField(auto_now_add=True, verbose_name="created at")

    class Meta:
        db_table = 'video'
        verbose_name = 'video'
        verbose_name_plural = 'videos'
        ordering = ['created_at']

    def __str__(self):
        return self.lesson.title
    

class CompletedLesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='completed_lessons', verbose_name="user", db_index=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               related_name='completed_by_users', verbose_name='lesson', db_index=True)
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="completed at")

    class Meta:
        db_table = 'completed_lesson'
        verbose_name = 'completed lesson'
        verbose_name_plural = 'completed lessons'
        unique_together = ('user', 'lesson')


class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='enrollments', verbose_name="user", db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='enrollments', verbose_name="course", db_index=True)

    created_at = models.DateField(auto_now_add=True, verbose_name="created at")

    class Meta:
        db_table = 'enrollment'
        verbose_name = 'enrollment'
        verbose_name_plural = 'enrollments'
        ordering = 'user', 'course', 'created_at'
        unique_together = ('course', 'user')


class PartEnrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='part_enrollments', verbose_name="user", db_index=True)
    part = models.ForeignKey('course.CoursePart', on_delete=models.CASCADE,
                             related_name='part_enrollments', db_index=True)

    created_at = models.DateField(auto_now_add=True, verbose_name="created at")

    class Meta:
        db_table = 'part_enrollment'
        verbose_name = 'part enrollment'
        verbose_name_plural = 'part enrollments'
        ordering = ['created_at']
        unique_together = ('part', 'user')


class CoursePart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='parts', db_index=True)
    order = models.PositiveSmallIntegerField(blank=True, verbose_name='order')

    class Meta:
        db_table = 'course_part'
        verbose_name = 'course part'
        verbose_name_plural = 'course parts'
        ordering = 'order',

    def __str__(self):
        return f'Part {self.order}'

    def save(self, *args, **kwargs):
        course_parts = self.course.parts.all()
        if not self.order:
            self.order = course_parts.count() + 1
        return super().save(*args, **kwargs)


class CourseBookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='bookmarks', verbose_name="user", db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='bookmarks', verbose_name="course", db_index=True)

    class Meta:
        db_table = 'course_bookmark'
        verbose_name = 'course bookmark'
        verbose_name_plural = 'course bookmarks'
        unique_together = ('user', 'course')

    def __str__(self):
        return "{}'s bookmark of {}".format(self.user, self.course)
