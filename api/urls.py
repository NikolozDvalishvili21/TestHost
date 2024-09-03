from django.urls import path, include
from .views import (BlogPageDetail, BlogPageListCreate, SliderPostsAPIView, SearchAPIView,
                    BlogPageByImageTagAPIView, AdvertisementPageDetail, AdvertisementPageList, QuizPageAPIView,
                    BlogPageByDotView)

urlpatterns = [
    path('cms/', include("wagtail.urls")),
    path('blogpages/', BlogPageListCreate.as_view(), name='blog_page_list'),
    path('blogpages/<int:custom_order>/', BlogPageDetail.as_view(), name='blog_page_detail'),
    path('slider-posts/', SliderPostsAPIView.as_view(), name='slider-posts-api'),
    path('search/', SearchAPIView.as_view(), name='search_api'),
    path('blogpages/tag/<str:tag>/', BlogPageByImageTagAPIView.as_view(), name='blogpages-by-image-tag'),
    path('advertisements/', AdvertisementPageList.as_view(), name='advertisement-list'),
    path('advertisements/<int:pk>/', AdvertisementPageDetail.as_view(), name='advertisement-detail'),
    path('quizzes/', QuizPageAPIView.as_view(), name='quiz-list'),
    path('category/<str:dot>/', BlogPageByDotView.as_view(), name='category-filter'),
]



