#author_by zhuxiaoliang
#2018-11-12 下午11:52

from django.urls import path,re_path
from .views import Index,index2,book_delete,book_edit,book_list
from .views import Bookviewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('book',Bookviewset)


app_name = 'drfapp'

urlpatterns = [
    path('index/',Index.as_view(),name='index'),
    path('index2/',index2,name='index2'),
    re_path('book_delete/(\d+)/',book_delete,name='book_delete'),
    re_path('book_edit/(\d+)/',book_edit,name='book_edit'),
    path('book_list/',book_list,name='book_list'),
    #path('books/',Bookviewset.as_view(),name='publisher-list')
]