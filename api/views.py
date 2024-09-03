import re

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.images.models import Image
from .models import BlogPage, AdvertisementPage, Quiz, Category
from .serializers import BlogPageSerializer, AdvertisementPageSerializer, QuizSerializer
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly
from django.db.models import Q


class QuizPageAPIView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)


class BlogPageListCreate(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = BlogPage.objects.all()
    serializer_class = BlogPageSerializer
    parser_classes = (MultiPartParser, FormParser)


class BlogPageDetail(generics.RetrieveAPIView):
    queryset = BlogPage.objects.all()
    serializer_class = BlogPageSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        # Retrieve the `custom_order` from the URL kwargs
        custom_order = self.kwargs.get('custom_order')

        # Get the BlogPage object with the specified custom_order
        obj = get_object_or_404(BlogPage, custom_order=custom_order)

        # Increment the view count
        obj.views += 1
        obj.save(update_fields=['views'])

        return obj


class SliderPostsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        slider_posts = BlogPage.objects.slider_posts()
        serializer = BlogPageSerializer(slider_posts, many=True)
        return Response(serializer.data)


class AdvertisementPageList(generics.ListAPIView):
    queryset = AdvertisementPage.objects.all()
    serializer_class = AdvertisementPageSerializer
    permission_classes = [AllowAny]


class AdvertisementPageDetail(generics.RetrieveAPIView):
    queryset = AdvertisementPage.objects.all()
    serializer_class = AdvertisementPageSerializer
    permission_classes = [AllowAny]


transliteration_map = {
    'a': 'ა', 'b': 'ბ', 'c': 'ც', 'd': 'დ', 'e': 'ე', 'f': 'ფ', 'g': 'გ', 'h': 'ჰ', 'i': 'ი',
    'j': 'ჯ', 'k': 'კ', 'l': 'ლ', 'm': 'მ', 'n': 'ნ', 'o': 'ო', 'p': 'პ', 'q': 'ქ', 'r': 'რ',
    's': 'ს', 't': 'ტ', 'u': 'უ', 'v': 'ვ', 'w': 'ვ', 'x': 'ხ', 'y': 'ი', 'z': 'ზ'
}


def transliterate_to_georgian(text):
    return ''.join(transliteration_map.get(char, char) for char in text)


class SearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('query', None)
        if search_query:
            normalized_query = search_query.lower()
            transliterated_query = transliterate_to_georgian(normalized_query)

            regex_patterns = [
                r'\b' + re.escape(normalized_query) + r'\b',
                r'\b' + re.escape(normalized_query[:-1]) + r'\S?\b',
                r'\b' + re.escape(normalized_query[:-2]) + r'\S{0,2}\b',
                r'\b' + re.escape(transliterated_query) + r'\b',
                r'\b' + re.escape(transliterated_query[:-1]) + r'\S?\b',
                r'\b' + re.escape(transliterated_query[:-2]) + r'\S{0,2}\b'
            ]

            # Filter using OR condition on the title and text fields
            search_results = BlogPage.objects.filter(
                Q(title__regex=regex_patterns[0]) | Q(text__regex=regex_patterns[0]) |
                Q(title__regex=regex_patterns[1]) | Q(text__regex=regex_patterns[1]) |
                Q(title__regex=regex_patterns[2]) | Q(text__regex=regex_patterns[2]) |
                Q(title__regex=regex_patterns[3]) | Q(text__regex=regex_patterns[3]) |
                Q(title__regex=regex_patterns[4]) | Q(text__regex=regex_patterns[4]) |
                Q(title__regex=regex_patterns[5]) | Q(text__regex=regex_patterns[5])
            )
        else:
            search_results = BlogPage.objects.all()

        serializer = BlogPageSerializer(search_results, many=True, context={'request': request})
        return Response(serializer.data)


class BlogPageByImageTagAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        tag = self.kwargs.get('tag', None)
        if tag:
            images_with_tag = Image.objects.filter(tags__name__in=[tag])
            blog_pages = BlogPage.objects.filter(image__in=images_with_tag)
        else:
            blog_pages = BlogPage.objects.none()

        serializer = BlogPageSerializer(blog_pages, many=True, context={'request': request})
        return Response(serializer.data)


class BlogPageByDotView(generics.ListAPIView):
    serializer_class = BlogPageSerializer

    def get_queryset(self):
        dot = self.kwargs.get('dot')
        return BlogPage.objects.filter(dot=dot)
