from django.urls import path

from .views import ReviewList, ReviewDetail

urlpatterns = [
    path('courses/<uuid:course_id>/reviews/', ReviewList.as_view(), name='course-reviews-list'),
    path('reviews/<uuid:review_id>/', ReviewDetail.as_view(), name='course-review-detail'),
]
