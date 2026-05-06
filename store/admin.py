from django.contrib import admin

# Register your models here.
# store/admin.py
from django.contrib import admin
from .models import Category, Book

admin.site.register(Category)
admin.site.register(Book)
