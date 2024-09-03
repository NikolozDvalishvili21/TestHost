from django.db import models
from django.db.models.signals import post_delete
from rest_framework.exceptions import ValidationError
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.documents.models import AbstractDocument
from wagtail.models import PageManager
from wagtail.fields import RichTextField
from wagtailvideos.models import Video
from wagtail.documents.models import Document


class BlogPageSignalHandler:
    @classmethod
    def reorder_blog_pages(cls, sender, instance, **kwargs):
        # Reorder pages with a higher custom_order
        subsequent_pages = BlogPage.objects.filter(custom_order__gt=instance.custom_order)
        for page in subsequent_pages:
            page.custom_order -= 1
            page.save()


class BlogPostQuerySet(models.QuerySet):
    def slider_posts(self):
        return self.filter(in_slider=True)[:7]


class BlogPostManager(PageManager.from_queryset(BlogPostQuerySet)):
    pass


CATEGORY_CHOICES = [
    ('#FF8CDF', 'პოლიტიკა'),
    ('#FFE500', 'საზოგადოება'),
    ('#00FA0A', 'ჯანმრთელობა'),
    ('#FF7A00', 'ეკონომიკა'),
    ('#FA00FF', 'კულტურა'),
    ('#FF0000', 'სპორტი'),
    ('#2500FF', 'ჩემი ქალაქი'),
    ('#8BF8FF', 'მსოფლიო'),
    ('#0094FF', 'ინტერვიუ'),
    ('#6B2000', 'გადაცემები'),
    ('#D9C2FF', 'ვიდეობლოგი'),
]

HEALTH_SUBCATEGORY_CHOICES = [
    ('nutrition', 'Nutrition'),
    ('mental_health', 'Mental Health'),
    ('exercise', 'Exercise'),
]


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)

    panels = [
        FieldPanel('name'),
        FieldPanel('color'),
    ]

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        'Category',
        related_name='subcategories',
        on_delete=models.CASCADE
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('parent_category'),
    ]

    def __str__(self):
        return self.name


class BlogPage(Page):
    custom_order = models.PositiveIntegerField(unique=True, null=True)
    in_slider = models.BooleanField(default=False, verbose_name="Include in slider")
    views = models.PositiveIntegerField(default=0, verbose_name="View Count")
    objects = BlogPostManager()
    date = models.DateTimeField("Post date")
    intro = models.CharField(max_length=255)
    text = RichTextField()
    image = models.ForeignKey(
        Image,
        on_delete=models.PROTECT,
        related_name='+'
    )

    video = models.ForeignKey(
        Video,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='v'
    )

    dot = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    subcategory = models.CharField(
        max_length=50,
        choices=HEALTH_SUBCATEGORY_CHOICES,
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('intro'),
            FieldPanel('text'),
            FieldPanel('image'),
            FieldPanel('video'),
            FieldPanel('dot'),
            FieldPanel('subcategory'),
            FieldPanel('in_slider'),
        ], heading="Blog information"),
    ]

    def clean(self):
        super().clean()
        if self.dot == '#00FA0A':  # If "ჯანმრთელობა" is selected
            if not self.subcategory:
                raise ValidationError('You must select a subcategory for "ჯანმრთელობა".')
        else:
            self.subcategory = None  # Clear subcategory if not "ჯანმრთელობა"

    def save(self, *args, **kwargs):
        if not self.custom_order:
            max_order = BlogPage.objects.aggregate(models.Max('custom_order'))['custom_order__max']
            self.custom_order = (max_order or 0) + 1

        super().save(*args, **kwargs)

    def get_category_name(self):
        return dict(CATEGORY_CHOICES).get(self.dot, 'Unknown')

    def get_subcategory_name(self):
        return dict(HEALTH_SUBCATEGORY_CHOICES).get(self.subcategory, 'No Subcategory')

    def __str__(self):
        return self.title


class AdvertisementPage(Page):
    AD_NUMBER_CHOICES = [
        (1, 'Position 1'),
        (2, 'Position 2'),
        (3, 'Position 3'),
        (4, 'Position 4'),
    ]
    ad_number = models.PositiveSmallIntegerField(choices=AD_NUMBER_CHOICES, unique=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    ad_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    ad_video = models.ForeignKey(
        Video,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    ad_gif = models.ForeignKey(
        Document, # Using Document for GIFs
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('ad_image'),
        FieldPanel('ad_video'),
        FieldPanel('ad_gif'),
        FieldPanel('link'),
        FieldPanel('ad_number')
    ]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ad_number'], name='unique_ad_number')
        ]

    def clean(self):
        super().clean()
        if sum(bool(field) for field in [self.ad_image, self.ad_video, self.ad_gif]) > 1:
            raise ValidationError('Only one of ad_image, ad_video, or ad_gif can be set.')

    def get_ad_media_url(self):
        if self.ad_image:
            return self.ad_image.file.url
        elif self.ad_video:
            # Ensure the file is properly associated with the video instance
            if not self.ad_video.file:
                raise ValidationError("The selected video has no associated file.")
            return self.ad_video.file.url
        elif self.ad_gif:
            return self.ad_gif.file.url
        return None


post_delete.connect(BlogPageSignalHandler.reorder_blog_pages, sender=BlogPage)


class Quiz(Page):
    question = models.CharField(max_length=255, null=True)
    image = models.ForeignKey(
        Image,
        on_delete=models.PROTECT,
        related_name='+',
        null=True
    )

    # Fixed number of answers
    answer1 = models.CharField(max_length=255, verbose_name="Answer 1", null=True)
    answer2 = models.CharField(max_length=255, verbose_name="Answer 2", null=True)
    answer3 = models.CharField(max_length=255, verbose_name="Answer 3", null=True)
    answer4 = models.CharField(max_length=255, verbose_name="Answer 4", null=True)

    # Field to indicate which answer is correct (1, 2, 3, or 4)
    correct_answer = models.IntegerField(choices=[(1, 'Answer 1'), (2, 'Answer 2'), (3, 'Answer 3'), (4, 'Answer 4')],
                                         verbose_name="Correct Answer", null=True)

    content_panels = Page.content_panels + [
        FieldPanel('question'),
        FieldPanel('image'),
        FieldPanel('answer1'),
        FieldPanel('answer2'),
        FieldPanel('answer3'),
        FieldPanel('answer4'),
        FieldPanel('correct_answer'),
    ]

    def get_quiz_data(self):
        # Return quiz data as a dictionary
        return {
            'question': self.question,
            'answers': [
                {'text': self.answer1, 'is_correct': self.correct_answer == 1},
                {'text': self.answer2, 'is_correct': self.correct_answer == 2},
                {'text': self.answer3, 'is_correct': self.correct_answer == 3},
                {'text': self.answer4, 'is_correct': self.correct_answer == 4},
            ]
        }

    def __str__(self):
        return self.question
