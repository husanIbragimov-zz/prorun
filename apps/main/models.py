from django.db import models
from django.utils.safestring import mark_safe

from apps.base.models import BaseModel


class BlogCategory(BaseModel):
    class Meta:
        verbose_name = "Blog Categories"
        verbose_name_plural = "Blog Category"

    title = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title


class News(models.Model):
    class Meta:
        verbose_name = "Newses"
        verbose_name_plural = "News"

    title = models.CharField(max_length=223, null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Partner(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    logo = models.ImageField(upload_to='partners/', null=True, blank=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.logo:
            return mark_safe(f'<a href="{self.logo.url}"><img src="{self.logo.url}" style="height:50px;"/></a>')
        return 'no_image'

