from rest_framework_simplejwt.authentication import JWTAuthentication
from UserData.models import Manga, UserProfile
from rest_framework.response import Response
from rest_framework.views import APIView
from UserData.serializers import MangaSerializer

# Create your views here.


class add_fav_manga(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = MangaSerializer(data=request.data)
        if serializer.is_valid():
            if Manga.objects.filter(
                manga_title=serializer.validated_data["manga_title"]
            ).exists():
                manga = Manga.objects.get(
                    manga_title=serializer.validated_data["manga_title"]
                )
                user = UserProfile.objects.get(user=request.user)
                if manga in user.favouriteMangas.all():
                    return Response({"message": "Manga already in favourites"})
                user.favouriteMangas.add(manga)
                user.save()
                return Response({"message": "Manga added to favourites"})
            else:
                manga = Manga.objects.create(
                    manga_title=serializer.validated_data["manga_title"],
                    manga_url=serializer.validated_data["manga_url"],
                    manga_image=serializer.validated_data["manga_image"],
                )
                
                manga.save()
                user = UserProfile.objects.get(user=request.user)
                user.favouriteMangas.add(manga)
                user.save()
                return Response({"message": "Manga added to favourites"})
        else:
            return Response({"message": "Invalid data"})


class get_fav_manga(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = UserProfile.objects.get(user=request.user)
        fav_manga = user.favouriteMangas.all()
        serializer = MangaSerializer(fav_manga, many=True)
        return Response(serializer.data)


class delete_fav_manga(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = MangaSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user = UserProfile.objects.get(user=request.user)
            manga = Manga.objects.filter(manga_title=serializer.validated_data["manga_title"])
            if manga.exists():
                manga = Manga.objects.get(
                    manga_title=serializer.validated_data["manga_title"]
                )
                user.favouriteMangas.remove(manga)
                user.save()
            else:
                return Response({"message": "Manga not found in favourites"})

            return Response({"message": "Manga removed from favourites"})
        else:
            return Response({"message": "Invalid data"})
