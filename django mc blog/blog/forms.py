from django import forms
from .models import Article
from django_summernote.widgets import SummernoteWidget

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'excerpt', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
        labels = {
            'title': 'Nadpis',
            'category': 'Kategorie',
            'excerpt': 'Krátký popisek',
            'content': 'Obsah článku',
        }