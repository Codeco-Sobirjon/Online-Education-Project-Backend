from django.urls import path

from .views import *

urlpatterns = [
    path('configs/', ConfigListView.as_view(), name='config-list'),
    path('configs/<str:key>/', ConfigDetailView.as_view(), name='config-detail'),

    path('faq-categories/', FAQCategoryListView.as_view(), name='faq-category-list'),
    path('faq-categories/<int:pk>/', FAQCategoryDetailView.as_view(), name='faq-category-detail'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),

    path('contacts/', ContactListView.as_view(), name='contact-list'),
    path('reports/', ReportListView.as_view(), name='report-list'),
]
