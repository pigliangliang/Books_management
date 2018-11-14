from django.db import models

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=128,unique=True)
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=32)
    state_provice = models.CharField(max_length=32)
    country = models.CharField(max_length=64)
    weisite = models.URLField()

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()

    def __str__(self):
        return self.first_name+self.last_name


class Book(models.Model):
    name = models.CharField(max_length=128)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher,on_delete=True)
    publish_date = models.DateField()

    def __str__(self):
        return self.name
