from django.urls import path

from .views.bookmark_views import CourseBookmarkView
from .views.category_views import CategoryDetail, CategoryList
from .views.course_views import CourseList, CourseDetail
from .views.enroll_views import PartEnrollView
from .views.lesson_views import LessonComplete, LessonList, LessonDetail
from .views.part_views import CoursePartDetailView
from .views.section_views import SectionDetail, SectionList
from .views.color_views import ColorList, ColorDetail

urlpatterns = [
    path('courses/', CourseList.as_view(), name='course-list'),
    path('courses/<uuid:course_id>/', CourseDetail.as_view(), name='course-detail'),
    path('courses/<uuid:course_id>/bookmark/', CourseBookmarkView.as_view(), name='course-bookmark'),

    path('course-parts/<uuid:part_id>/', CoursePartDetailView.as_view(), name='part-detail'),
    path('course-parts/<uuid:part_id>/enroll/', PartEnrollView.as_view(), name='part-enroll'),

    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<uuid:category_id>/', CategoryDetail.as_view(), name='category-detail'),

    path('courses/<uuid:course_id>/sections/', SectionList.as_view(), name='section-list'),
    path('sections/<uuid:section_id>/', SectionDetail.as_view(), name='section-detail'),

    path('sections/<uuid:section_id>/lessons/', LessonList.as_view(), name='lesson-list'),
    path('lessons/<uuid:lesson_id>/', LessonDetail.as_view(), name='lesson-detail'),
    path('lessons/<uuid:lesson_id>/complete/', LessonComplete.as_view(), name='lesson-complete'),

    path('colors/', ColorList.as_view(), name='color-list'),
    path('colors/<uuid:color_id>/', ColorDetail.as_view(), name='color-detail'),
]
