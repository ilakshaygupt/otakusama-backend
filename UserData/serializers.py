from rest_framework import serializers

from UserData.models import Manga





class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ["manga_title", "manga_url", "manga_image"]
