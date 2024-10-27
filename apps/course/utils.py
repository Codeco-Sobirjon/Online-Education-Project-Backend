from django.contrib.contenttypes.models import ContentType


def reordering_sections(sections):

    for num, section in enumerate(sections):
        content_type = ContentType.objects.get_for_model(section)
        obj = content_type.model_class().objects.filter(id=section.id)
        order = num + 1
        obj.update(order=order)


def reordering_lessons(lessons):

    for num, lesson in enumerate(lessons):
        content_type = ContentType.objects.get_for_model(lesson)
        obj = content_type.model_class().objects.filter(id=lesson.id)
        order = num + 1
        obj.update(order=order)


def parting_course(course, lessons):
    lessons_count = course.lesson_count
    lessons_per_part = course.part_lesson_count
    course_part_model = ContentType.objects.get(app_label="course", model="coursepart").model_class()
    
    for start_index in range(0, lessons_count, lessons_per_part):
        end_index = start_index + lessons_per_part
        order = start_index // lessons_per_part + 1
        part, created = course_part_model.objects.get_or_create(course=course, order=order)
        part.lessons.clear()
        part.lessons.add(*lessons[start_index: end_index])

    last_order = (lessons_count - 1) // lessons_per_part + 1
    course_part_model.objects.filter(course=course, order__gt=last_order).delete()
