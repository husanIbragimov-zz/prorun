from django.contrib import admin
from apps.main.models import News, Partner, BlogCategory


@admin.register(News)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')


admin.site.register(Partner)
admin.site.register(BlogCategory)
