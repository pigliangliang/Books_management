#author_by zhuxiaoliang
#2018-11-12 下午11:42

from django.forms import ModelForm
from django import forms
from .models import Book


class BookModelForm(ModelForm):
    class Meta:
        model =Book

        fields = '__all__'
        labels = {
            'name': '图书名',
            'author': '作者',
            'publisher':'出版社',
            'publish_date':'出版日期',
        }

