from bs4 import BeautifulSoup
from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def search_manga(request):
    if request.method == "POST":
        text = request.data.get("text")
        if text is None:
            return Response(
                {"error": "No 'text' parameter found in request."}, status=400
            )
        text = text.split(" ")
        text = "_".join(text)
        url = f"https://manganato.com/search/story/{text}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        search_items = soup.find_all("div", class_="search-story-item")
        results = []
        for item in search_items:
            author = (
                item.find("span", class_="item-author").text
                if item.find("span", class_="item-author")
                else ""
            )
            updated_time = (
                item.find("span", class_="item-time").text
                if item.find("span", class_="item-time")
                else ""
            )
            image = item.find("img")["src"] if item.find("img") else ""
            title = item.find("h3").text if item.find("h3") else ""
            access_link = item.find("a")["href"] if item.find("a") else ""
            last_chapter = item.find("a", class_="item-chapter")
            if last_chapter is not None:
                last_chapter = last_chapter.text
            else:
                last_chapter = ""
            result = {
                "author": author,
                "updated_time": updated_time,
                "image": image,
                "title": title,
                "last_chapter": last_chapter,
                "access_link": access_link,
            }
            results.append(result)
        return Response(results)


@api_view(["POST"])
def get_manga_list(request):
    if request.method == "POST":
        url = request.data.get("url")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        manga_list = BeautifulSoup(response.content, "html.parser").find_all(
            "a", class_="chapter-name text-nowrap"
        )
        # For Extracting Manga Information
        manga_info = soup.find("div", class_="panel-story-info")

        # Extracting Manga Title
        title = manga_info.find("h1").text

        # Extracting Manga Alternative Title
        alterative = (
            manga_info.find("h2").text if manga_info.find("h2") is not None else ""
        )

        # Extracting Manga Authors
        author_tags = soup.find_all("i", class_="info-author")

        author_data = []
        for author_tag in author_tags:
            author_links = author_tag.find_next("td", class_="table-value").find_all(
                "a"
            )

            author_names = [author_link.text for author_link in author_links]
            author_links = [author_link["href"] for author_link in author_links]
            for i in range(len(author_names)):
                author_name = author_names[i]
                author_link = author_links[i]
                if author_name not in author_data:
                    author_data.append({"name": author_name, "link": author_link})

        # Extracting Manga Status
        status = soup.find("i", class_="info-status").find_next("td").text

        # Extracting Manga Genres
        genres_tags = soup.find_all("i", class_="info-genres")

        genres_data = []
        for genre in genres_tags:
            genre_link = genre.find_next("td", class_="table-value").find_all("a")
            genre_name = [genre.text for genre in genre_link]
            genre_link = [genre["href"] for genre in genre_link]

            for genre_name, genre_link in zip(genre_name, genre_link):

                if genre_name not in genres_data:
                    genres_data.append({"name": genre_name, "link": genre_link})

        # Extracting Manga Updated Time
        updated_time = (
            soup.find("i", class_="info-time")
            .find_next("span", class_="stre-value")
            .text
        )

        # Extracting Manga View Count
        view_count = (
            soup.find("i", class_="info-view")
            .find_next("span", class_="stre-value")
            .text
        )

        # Extracting Manga Rating
        rating = soup.find("em", property="v:average").text

        # wxtracting description
        description = soup.find("div", class_="panel-story-info-description").find_all(
            text=True,
        )

        description = " ".join(description)
        # extracting image

        image_link = soup.find("div", class_="story-info-left").find("img")["src"]

        # Use the extracted information as needed
        listAll = []
        for manga in manga_list:
            managa_link = manga["href"]
            manga_text = manga.text
            listAll.append({"mangaLink": managa_link, "mangaText": manga_text})
        return JsonResponse(
            {
                "title": title,
                "alternative": alterative,
                "authors": author_data,
                "status": status,
                "genres": genres_data,
                "updatedTime": updated_time,
                "viewCount": view_count,
                "rating": rating,
                "description": description,
                "imageLink": image_link,
                "mangaList": listAll,
            },
            safe=False,
        )


@api_view(["POST"])
def get_manga_detail(request):
    url = request.data.get("url")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    all_images = soup.find_all("div", class_="container-chapter-reader")
    img_tags = [img_tag for div in all_images for img_tag in div.find_all("img")]
    alling = []
    for img_tag in img_tags:
        alling.append(img_tag["src"])

    return JsonResponse({"data": alling})


@api_view(["GET"])
def get_top_manga(request):
    url = "https://manganato.com/genre-all?type=topview"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    top_manga = soup.find_all("div", class_="content-genres-item")
    results = []
    for item in top_manga:
        author = (
            item.find("span", class_="genres-item-author").text
            if item.find("span", class_="genres-item-author")
            else ""
        )
        updated_time = (
            item.find("span", class_="genres-item-time").text
            if item.find("span", class_="genres-item-time")
            else ""
        )
        image = item.find("img")["src"] if item.find("img") else ""
        title = item.find("h3").text if item.find("h3") else ""
        access_link = item.find("a")["href"] if item.find("a") else ""
        last_chapter = (
            item.find("a", class_="genres-item-chap text-nowrap a-h")
            if item.find("a", class_="genres-item-chap text-nowrap a-h")
            else ""
        )
        if last_chapter is not None:
            last_chapter = last_chapter.text
        else:
            last_chapter = ""
        result = {
            "author": author,
            "updated_time": updated_time,
            "image": image,
            "title": title,
            "last_chapter": last_chapter,
            "access_link": access_link,
        }

        results.append(result)

    return JsonResponse(results, safe=False)


@api_view(["GET"])
def get_latest_manga(request):
    url = "https://manganato.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    latest_manga = soup.find_all("div", class_="content-homepage-item")
    print(latest_manga[:5])
    results = []
    for item in latest_manga:
        author = (
            item.find("span", class_="item-author").text.strip()
            if item.find("span", class_="item-author")
            else ""
        )

        updated_time = item.find("i").text.strip() if item.find("i") else ""
        image = item.find("img")["src"] if item.find("img") else ""
        title = item.find("h3").text.strip() if item.find("h3") else ""
        access_link = item.find("a")["href"] if item.find("a") else ""

        last_chapter = (
            item.find("span", class_="text-nowrap item-author").text
            if item.find("span", class_="text-nowrap item-author")
            else ""
        )
        print(last_chapter)

        manga = {
            "author": author,
            "updated_time": updated_time,
            "image": image,
            "title": title,
            "last_chapter": last_chapter,
            "access_link": access_link,
        }

        results.append(manga)

    return JsonResponse(results, safe=False)
