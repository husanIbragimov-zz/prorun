from rest_framework import serializers
from apps.main.models import News, Partner, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('id', 'title')


class NewsDefaultSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(many=False)

    class Meta:
        model = News
        fields = ('id', 'title', 'category', 'image', 'created_at')


class NewsSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(many=False)

    class Meta:
        model = News
        fields = ('id', 'title', 'image', 'category', 'description', 'created_at')


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ('id', 'name', 'logo')
