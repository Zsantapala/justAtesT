from django.contrib import admin
from .models import User, Article
# Register your models here.
admin.site.register(User)
admin.site.register(Article)