from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Article

# Tímto řekneme, že pole 'content' má v administraci používat Summernote
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)