from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.article.models import Post
from apps.article.forms import PostForm

from django.core.paginator import Paginator

from .models import Profile
from .forms import ProfileForm

# Create your views here.
def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have been logged in')
            return redirect('main:index')
        else:
            messages.error(request, 'Error logging in')
    
    return render(request, 'members/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('main:index')


def signup_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user)
            profile.save()
            login(request, user)
            messages.success(request, 'You have been signed up')
            return redirect('main:index')
        else:
            messages.error(request, 'Error signing up')
            
    return render(request, 'members/signup.html', {'form': form})


@login_required
def profile_view(request, pk):
    profile = get_object_or_404(Profile.objects.select_related('user', 'user__profile'), pk=pk)
    posts = Post.objects.filter(author=profile.user).select_related("author", 'author__profile').prefetch_related("like", "dislike", "comments", "tags")

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'is_owner': request.user == profile.user,
        'profile': profile,
        'posts': posts,
        'created_form': PostForm(),
    }

    return render(request, 'members/profile.html', context)


@login_required
def profile_edit_view(request):
    profile = Profile.objects.select_related('user').get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile is updated')
            return redirect('members:profile', pk=profile.pk)
        else:
            messages.error(request, 'Error updating profile')
    else:
        form = ProfileForm(instance=profile)
     
    return render(request, 'members/profile_edit.html', {'form': form})
