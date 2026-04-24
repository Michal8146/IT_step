from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login # Toto chybělo
from django.contrib.auth.models import User         # Toto chybělo
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.shortcuts import get_object_or_404
from blog.models import Article

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'Účet pro {user.username} byl vytvořen! Nyní se můžeš přihlásit.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user_exists = User.objects.filter(username=username).exists()
        
        if not user_exists:
            # Zůstaneme na login.html a pošleme informaci, že hráč neexistuje
            messages.warning(request, f'Hráč "{username}" nebyl nalezen. Chceš si vytvořit nový účet?')
            return render(request, 'users/login.html', {'show_register_link': True, 'username': username})
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Špatné heslo! Zkus to znovu.')
            return render(request, 'users/login.html', {'username': username})
            
    return render(request, 'users/login.html')

@login_required
def profile(request):
    # Bezpečnostní pojistka: vytvoří profil, pokud chybí (např. u admina vytvořeného před signály)
    Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # request.FILES je extrémně důležité pro ukládání obrázků!
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Tvůj profil byl úspěšně zaktualizován!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


def user_profile(request, username):
    # Najde uživatele podle jména, nebo hodí chybu 404
    profile_user = get_object_or_404(User, username=username)
    # Najde všechny články, které tento uživatel napsal
    user_articles = Article.objects.filter(author=profile_user).order_by('-created_at')
    
    return render(request, 'users/public_profile.html', {
        'profile_user': profile_user,
        'user_articles': user_articles
    })