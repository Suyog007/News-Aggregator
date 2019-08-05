from django.contrib import admin
from .models  import News, Category
from django.db import models
from django.forms import TextInput, Textarea


class news_admin(admin.ModelAdmin):
     readonly_fields = ('id',)
     formfield_overrides = {
         models.CharField: {'widget': Textarea(attrs={'rows':15, 'cols':100})},
       
    }




# Register your models here.
admin.site.register(News, news_admin)
admin.site.register(Category)
