from rest_framework import serializers

class ImageHashSerializer(serializers.Serializer):
    hash1 = serializers.CharField(required=False)
    hash2 = serializers.CharField(required=False)
    