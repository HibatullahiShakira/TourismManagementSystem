from rest_framework import serializers


class TourSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, allow_blank=False)
    description = serializers.CharField(max_length=1500, allow_blank=False)
    location = serializers.CharField(max_length=100, allow_blank=False)
    images = serializers.ImageField(allow_null=True, required=False)
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    availability = serializers.BooleanField(default=True)
