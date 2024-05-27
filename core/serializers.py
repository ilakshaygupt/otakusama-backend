
from rest_framework import serializers

class MangaSearchSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('text')