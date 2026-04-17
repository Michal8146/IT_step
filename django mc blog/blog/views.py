from django.shortcuts import render, get_object_or_404
from .models import Article

def home_view(request):
    # Získáme všechny články, seřazené od nejnovějšího
    articles = Article.objects.all().order_by('-created_at')
    
    context = {
        'articles': articles
    }
    return render(request, 'blog/home.html', context)

def article_detail(request, id):
    # Najde článek podle ID, nebo vyhodí chybovou stránku 404
    article = get_object_or_404(Article, id=id)
    
    context = {
        'article': article
    }
    return render(request, 'blog/article_detail.html', context)