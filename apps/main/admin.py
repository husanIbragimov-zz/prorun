from django.contrib import admin
from apps.main.models import News, Partner, BlogCategory


@admin.register(News)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    readonly_fields = ['image_tag']


admin.site.register(Partner, PartnerAdmin)
admin.site.register(BlogCategory)
