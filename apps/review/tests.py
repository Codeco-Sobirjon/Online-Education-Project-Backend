from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from course.models import Course, Category, Color
from review.models import Review

User = get_user_model()


class ReviewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='test_user', password='test_pass', email='testuser@example.com'
        )

        login_url = reverse('User login')
        response = self.client.post(login_url, {'username': 'test_user', 'password': 'test_pass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.category = Category.objects.create(name='Test Category')
        self.color1 = Color.objects.create(name='Red', hex_code='#FF0000')
        self.color2 = Color.objects.create(name='Blue', hex_code='#0000FF')

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            category=self.category,
            teacher=self.user,
            image='path/to/image.jpg',
            video='path/to/video.mp4',
            color1=self.color1,
            color2=self.color2
        )

        self.review_data = {
            'comment': 'Great course!',
            'rating': 5,
        }

    def test_create_review(self):
        url = reverse('course-reviews-list', kwargs={'course_id': self.course.id})
        response = self.client.post(url, self.review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().comment, 'Great course!')

    def test_create_duplicate_review(self):
        url = reverse('course-reviews-list', kwargs={'course_id': self.course.id})
        self.client.post(url, self.review_data, format='json')
        response = self.client.post(url, self.review_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_reviews(self):
        Review.objects.create(course=self.course, user=self.user, comment='Nice course!', rating=4)
        url = reverse('course-reviews-list', kwargs={'course_id': self.course.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['comment'], 'Nice course!')

    def test_update_review(self):
        review = Review.objects.create(course=self.course, user=self.user, comment='Nice course!', rating=4)
        url = reverse('course-review-detail', kwargs={'review_id': review.id})
        updated_data = {'comment': 'Updated comment', 'rating': 5}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.comment, 'Updated comment')
        self.assertEqual(review.rating, 5)

    def test_delete_review(self):
        review = Review.objects.create(course=self.course, user=self.user, comment='Nice course!', rating=4)
        url = reverse('course-review-detail', kwargs={'review_id': review.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)

    def test_rating_out_of_bounds(self):
        url = reverse('course-reviews-list', kwargs={'course_id': self.course.id})
        invalid_data = {
            'comment': 'Bad rating',
            'rating': 6,
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_data['rating'] = -1
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
