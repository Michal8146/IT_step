from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article
from .forms import ArticleForm
from comments.models import Comment
from comments.forms import CommentForm

def home_view(request):
    # Získáme všechny články, seřazené od nejnovějšího
    articles = Article.objects.all().order_by('-created_at')
    
    context = {
        'articles': articles
    }
    return render(request, 'blog/home.html', context)

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    # Získáme všechny komentáře k tomuto článku seřazené od nejnovějších
    comments = article.comments.all().order_by('-created_at')

    if request.method == 'POST':
        # Bezpečnostní pojistka: odeslat formulář může jen přihlášený
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article       # Přiřadíme k aktuálnímu článku
                comment.author = request.user   # Přiřadíme aktuálního uživatele
                comment.save()
                messages.success(request, 'Tvůj komentář byl přidán!')
                return redirect('article_detail', id=article.id)
    else:
        form = CommentForm()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user # Automaticky přiřadí autora
            article.save()
            messages.success(request, 'Tvůj článek byl úspěšně publikován!')
            return redirect('article_detail', id=article.id)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form, 'title': 'Napsat nový článek'})

@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    
    # Zabezpečení: Upravovat může jen autor nebo moderátor (is_staff)
    if article.author != request.user and not request.user.is_staff:
        messages.error(request, 'Nemáš oprávnění upravovat tento článek.')
        return redirect('article_detail', id=id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Článek byl úspěšně upraven!')
            return redirect('article_detail', id=article.id)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form, 'title': 'Upravit článek'})

@login_required
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    
    # Zabezpečení: Smazat může jen autor nebo moderátor
    if article.author != request.user and not request.user.is_staff:
        messages.error(request, 'Nemáš oprávnění smazat tento článek.')
        return redirect('article_detail', id=id)

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Článek byl smazán.')
        return redirect('home')
    
    return render(request, 'blog/article_confirm_delete.html', {'article': article})


@login_required
def like_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.user in article.likes.all():
        article.likes.remove(request.user) # Odlajkování
    else:
        article.likes.add(request.user)    # Lajkování
    # Vrátí uživatele zpět na stránku, kde kliknul (např. detail článku)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def like_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))