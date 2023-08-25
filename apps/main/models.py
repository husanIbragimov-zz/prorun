from django.db import models


class News(models.Model):
    class Meta:
        verbose_name = "Newses"
        verbose_name_plural = "News"

    title = models.CharField(max_length=223, null=True, blank=True)
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
