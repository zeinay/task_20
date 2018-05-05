from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from restaurants.models import Restaurant
from .views import (
    RestaurantListView,
    RestaurantDetailView,
    RestaurantCreateView,
    RestaurantUpdateView,
    RestaurantDeleteView,
)

class RestaurantAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create(
            username="bob",
            password='adminadmin',
            is_staff=True,
            )
        self.user.set_password(self.user.password)
        self.user.save()
        self.user2 = User.objects.create(
            username="bob2",
            password='adminadmin',
            )
        self.user2.set_password(self.user2.password)
        self.user2.save()
        self.user3 = User.objects.create(
            username="bob3",
            password='adminadmin',
            )
        self.user3.set_password(self.user3.password)
        self.user3.save()

        self.restaurant_1 = Restaurant.objects.create(
            owner=self.user,
            name="Restaurant 1",
            description="This is Restaurant 1",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )
        self.restaurant_2 = Restaurant.objects.create(
            owner=self.user2,
            name="Restaurant 2", 
            description="This is Restaurant 2",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )

        self.restaurant_data = {
            "owner":self.user,
            "name":"Restaurant 1", 
            "description":"This is Restaurant 1 updated",
            "opening_time":"00:01:00",
            "closing_time":"23:59:00",
        }

    def test_restaurant_list_view(self):
        list_url = reverse("api-list")
        request = self.factory.get(list_url)
        response = RestaurantListView.as_view()(request)
        expected = [
                {
                    'name':self.restaurant_1.name,
                    'opening_time': self.restaurant_1.opening_time,
                    'closing_time': self.restaurant_1.closing_time,
                    'detail': "http://"+ request.get_host()+reverse("api-detail", kwargs = {"restaurant_id": self.restaurant_1.id}),
                    'update': "http://"+ request.get_host()+reverse("api-update", kwargs = {"restaurant_id": self.restaurant_1.id}),
                    'delete': "http://"+ request.get_host()+reverse("api-delete", kwargs = {"restaurant_id": self.restaurant_1.id})
                },
                {
                    'name':self.restaurant_2.name,
                    'opening_time': self.restaurant_2.opening_time,
                    'closing_time': self.restaurant_2.closing_time,
                    'detail': "http://"+ request.get_host()+reverse("api-detail", kwargs = {"restaurant_id": self.restaurant_2.id}),
                    'update': "http://"+ request.get_host()+reverse("api-update", kwargs = {"restaurant_id": self.restaurant_2.id}),
                    'delete': "http://"+ request.get_host()+reverse("api-delete", kwargs = {"restaurant_id": self.restaurant_2.id})
                },
            ]
        self.assertEqual(
            expected,
            response.data
        )
        self.assertEqual(response.status_code, 200)

    def test_restaurant_detail_view(self):
        detail_url = reverse("api-detail", kwargs = {"restaurant_id": self.restaurant_1.id})
        request = self.factory.get(detail_url)
        response = RestaurantDetailView.as_view()(request, restaurant_id=self.restaurant_1.id)
        self.assertEqual(
            {
                'id':self.restaurant_1.id,
                'owner':self.restaurant_1.owner.id,
                'name':self.restaurant_1.name,
                'description':self.restaurant_1.description,
                'opening_time': self.restaurant_1.opening_time,
                'closing_time': self.restaurant_1.closing_time,
                'update': "http://"+ request.get_host()+reverse("api-update", kwargs = {"restaurant_id": self.restaurant_1.id}),
                'delete': "http://"+ request.get_host()+reverse("api-delete", kwargs = {"restaurant_id": self.restaurant_1.id})
            },
            response.data
        )
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        create_url = reverse("api-create")
        request = self.factory.post(create_url, data=self.restaurant_data)
        response = RestaurantCreateView.as_view()(request)
        self.assertEqual(response.status_code, 403)

        force_authenticate(request, user=self.user)
        response = RestaurantCreateView.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 3)

    def test_restaurant_update_view(self):
        update_url = reverse("api-update", kwargs = {"restaurant_id": self.restaurant_2.id})
        request = self.factory.put(update_url, data=self.restaurant_data)
        response = RestaurantUpdateView.as_view()(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response.status_code, 403)

        force_authenticate(request, user=self.user)
        response = RestaurantUpdateView.as_view()(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response.status_code, 200)

        force_authenticate(request, user=self.user2)
        response = RestaurantUpdateView.as_view()(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response.status_code, 200)

        force_authenticate(request, user=self.user3)
        response = RestaurantUpdateView.as_view()(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response.status_code, 403)

    def test_restaurant_delete_view(self):
        delete_url = reverse("api-delete", kwargs = {"restaurant_id": self.restaurant_2.id})
        request = self.factory.delete(delete_url)
        response1 = RestaurantDeleteView.as_view()(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response1.status_code, 403)

        force_authenticate(request, user=self.user)
        response = RestaurantDeleteView.as_view()(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response.status_code, 204)

        force_authenticate(request, user=self.user2)
        response = RestaurantDeleteView.as_view()(request, restaurant_id=self.restaurant_2.id)
        self.assertEqual(response.status_code, 403)