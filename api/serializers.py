from rest_framework import serializers
from restaurants.models import Restaurant, Item
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price',]

class RestaurantListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )
    update = serializers.HyperlinkedIdentityField(
        view_name = "api-update",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )
    delete = serializers.HyperlinkedIdentityField(
        view_name = "api-delete",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )

    class Meta:
        model = Restaurant
        fields = [
            'name',
            'opening_time',
            'closing_time',
            'detail',
            'update',
            'delete',
            ]


class RestaurantDetailSerializer(serializers.ModelSerializer):
    update = serializers.HyperlinkedIdentityField(
        view_name = "api-update",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )
    delete = serializers.HyperlinkedIdentityField(
        view_name = "api-delete",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )
    owner = UserSerializer()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'owner',
            'name',
            'description',
            'opening_time',
            'closing_time',
            'update',
            'delete',
            'items',
            ]

    def get_items(self, obj):
        items = Item.objects.filter(restaurant=obj)
        item_list = ItemSerializer(items, many=True).data
        return item_list

class RestaurantCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'name',
            'description',
            'opening_time',
            'closing_time',
            ]