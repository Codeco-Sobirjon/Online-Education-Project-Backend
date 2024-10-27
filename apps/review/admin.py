from django.contrib import admin

from apps.review.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'comment', 'rating')
    list_filter = ('course', 'user')
    fields = ('user', 'course', 'rating', 'comment', 'created_at')
    readonly_fields = 'created_at',
