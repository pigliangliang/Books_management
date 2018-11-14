#author_by zhuxiaoliang
#2018-11-10 下午10:52

from django.contrib.auth.models import User,Group
from rest_framework import serializers

from .models import Book

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User

        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url','name')


class  BookSerializer(serializers.ModelSerializer):
    publisher = serializers.StringRelatedField(source='publisher.name')
    #author = serializers.StringRelatedField(source='author.first_name')
    class Meta:
        model = Book

        fields = ('name','author','publisher','publish_date')
