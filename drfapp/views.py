from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User,Group
from rest_framework import viewsets
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .serializers import GroupSerializer,UserSerializer

from django.views.generic.base import TemplateView
from rest_framework.generics import views
from .forms import BookModelForm
from .models import Book
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from .serializers import BookSerializer
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticated





class Userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')

    serializer_class = UserSerializer

class Groupviewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class Index(TemplateView):

    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        info = Book.objects.all().values_list('id','name','author__first_name','author__last_name','publish_date','publisher__name')
        print(info)
        d = {}
        for i in info:
            if i[1] not in d.keys():
                d[i[1]] = {
                    'id':i[0],
                    'auth':[i[2]+i[3]],
                    'datatime':i[4],
                    'pub':i[5],
                }
            else:
                d[i[1]]['auth'].append(i[2]+i[3])
        print('0000', d.items())
        form = BookModelForm()
        return render_to_response('index.html',{'form':form,'d':d})

    def post(self,request):
        form = BookModelForm(request.POST)
        print(form.data.get('author'))
        try:
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('drfapp:index'))
            else:
                print(form.errors)
                return HttpResponse(form.errors)
        except Exception as e:
            print(e)
            return HttpResponse('error')

def index2(request):
    if request.method=="POST":
        form = BookModelForm(request.POST)

        if form.is_valid():
            form.save()
            return  HttpResponse('ok')
        else:

            return HttpResponse(form.errors)
    else:

        form  = BookModelForm()
        return  render_to_response('index.html',{'form':form})


def book_delete(request,id):
    print(request.method)
    Book.objects.get(id=id).delete()
    return  HttpResponseRedirect(reverse('drfapp:index'))


def book_edit(request,id):

    if request.method=="GET":
        book = Book.objects.get(id=id)
        bf = BookModelForm(instance=book)
        return render_to_response('book_edit.html',{'bf':bf})
    else:
        print(request.POST)
        bf = BookModelForm(request.POST)
        if bf.is_valid():
            print(bf.cleaned_data)

            #修改一个表中存在一对多和多对多关系的数据
            """
            1、先处理一对多的数据，一对多的字段是一个实例，当前表的实例更新过程如下语句二。
            2、更新多对多数据
                准备好多对多字段的数据，多对多字段的数据是一个queryset ,如：'author': <QuerySet [<Author: 钱八>]>, 
                准备当前表的实例，通过实例.多对多字段.add()方法进行添加数据
            """
            publisher = bf.cleaned_data['publisher']
            #语句一
            Book.objects.filter(id=id).update(name=bf.cleaned_data['name'],publish_date=bf.cleaned_data['publish_date'],publisher=publisher)
            book = Book.objects.get(id=id)
            book.author.clear()
            for auth in bf.cleaned_data['author']:
                book.author.add(auth)

        return HttpResponseRedirect(reverse('drfapp:index'))

def book_list(request):
    if request.method=="GET":
        books = Book.objects.all()
        serialiser = BookSerializer(books,many=True)
        print(serialiser)
        return HttpResponse(serialiser.data)
        #return JsonResponse(serialiser.data,content_type='application/json',safe=False)
from rest_framework import permissions
class Bookviewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)