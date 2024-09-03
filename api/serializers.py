from rest_framework import serializers
from blogSite.settings.base import BASE_URL
from .models import BlogPage, AdvertisementPage, Quiz
from wagtail.images.models import Image
from wagtailvideos.models import Video


class ImageSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['title', 'file', 'tags']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.file.url
            if request:
                return request.build_absolute_uri(url)
            else:
                return BASE_URL + url  # Fallback if request is not available
        return None

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


class VideoSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['file', 'thumbnail']

    def get_video_url(self, obj):
        if obj.video:
            return obj.video.file.url
        return None

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            url = obj.thumbnail.url
            if request:
                return request.build_absolute_uri(url)
            else:
                return BASE_URL + url  # Fallback if request is not available
        return None


class BlogPageSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    video = VideoSerializer()
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.get_category_name()

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d")

    def get_time(self, obj):
        return obj.date.strftime("%H:%M:%S")

    class Meta:
        model = BlogPage
        fields = ['custom_order', 'title', 'views', 'date', 'time', 'intro', 'text', 'dot', 'category_name', 'image',
                  'video', 'in_slider', 'subcategory']


class AdvertisementPageSerializer(serializers.ModelSerializer):
    ad_media_url = serializers.SerializerMethodField()

    class Meta:
        model = AdvertisementPage
        fields = ['ad_media_url', 'link', 'ad_number']

    def get_ad_media_url(self, obj):
        request = self.context.get('request')
        media_url = obj.get_ad_media_url()
        if media_url:
            return request.build_absolute_uri(media_url)
        return None

    def validate_ad_number(self, value):
        # Check if the number is within the allowed range (1-4)
        if value not in range(1, 5):
            raise serializers.ValidationError("Ad number must be between 1 and 4.")

        # Check if an advertisement with this number already exists
        if AdvertisementPage.objects.filter(ad_number=value).exists():
            raise serializers.ValidationError(f"Advertisement with ad number {value} already exists.")

        return value


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ['question', 'answer1', 'answer2', 'answer3', 'answer4', 'correct_answer']
