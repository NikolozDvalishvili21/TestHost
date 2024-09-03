from django.contrib import admin
from .models import BlogPage, AdvertisementPage, Video


class blogAdmin(admin.ModelAdmin):
    list_display = ('custom_order', 'title', 'date', 'intro', 'dot')


admin.site.register(BlogPage, blogAdmin)
admin.site.register(AdvertisementPage)
admin.site.register(Video)
