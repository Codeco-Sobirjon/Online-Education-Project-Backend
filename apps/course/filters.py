import django_filters.rest_framework as filters
from django.db.models import Count, Avg, F, Case, When
from django.db.models.functions import Round

from apps.course.models import Course

POPULAR_COURSES_COUNT = 10


class CourseFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__name', lookup_expr='exact')
    teacher_id = filters.CharFilter(field_name='teacher__id', lookup_expr='exact')
    enrolled = filters.BooleanFilter(method='filter_enrolled')
    popular = filters.BooleanFilter(method='filter_popular')
    rating = filters.NumberFilter(method='filter_rating')
    price = filters.NumericRangeFilter(method='filter_price')
    bookmarked = filters.BooleanFilter(method='filter_bookmarked')
    completed = filters.BooleanFilter(method='filter_completed')

    class Meta:
        model = Course
        fields = ['search', 'category', 'teacher_id', 'enrolled', 'popular', 'rating', 'price']

    def filter_enrolled(self, queryset, _, value):
        user = self.request.user
        if not user or not user.is_authenticated:
            return queryset.none()

        if value is True:
            return queryset.filter(enrollments__user=user)
        elif value is False:
            return queryset.exclude(enrollments__user=user)
        return queryset

    def filter_popular(self, queryset, _, value):
        if value is True:
            return queryset.annotate(count=Count('enrollments')).order_by('-count')[:POPULAR_COURSES_COUNT]
        return queryset

    def filter_rating(self, queryset, _, value):
        queryset = queryset.annotate(avg_rating=Round(Avg('reviews__rating')))
        return queryset.filter(avg_rating=value)

    def filter_price(self, queryset, _, value):
        queryset = queryset.annotate(
            _lesson_count=Count('sections__lessons')
        ).annotate(
            _price=F('_lesson_count') * F('lesson_price')
        ).annotate(
            _discounted_price=F('_lesson_count') * F('discounted_lesson_price')
        ).annotate(
            conditional_price=Case(
                When(_discounted_price__isnull=False, then=F('_discounted_price')),
                When(_discounted_price__isnull=True, then=F('_price'))
            )
        )

        if value.start:
            queryset = queryset.filter(conditional_price__gte=value.start)
        if value.stop:
            queryset = queryset.filter(conditional_price__lte=value.stop)

        return queryset

    def filter_bookmarked(self, queryset, _, value):
        user = self.request.user
        if not user or not user.is_authenticated:
            return queryset.none() if value else queryset

        if value is True:
            return queryset.filter(bookmarks__user=user)
        elif value is False:
            return queryset.exclude(bookmarks__user=user)
        return queryset

    def filter_completed(self, queryset, _, value):
        user = self.request.user
        if not user or not user.is_authenticated:
            return queryset.none() if value else queryset

        if value is True:
            return queryset.filter(reviews__user=user)
        elif value is False:
            return queryset.exclude(reviews__user=user)
        return queryset
