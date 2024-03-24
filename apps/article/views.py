from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm

from django.contrib import messages

from django.core.paginator import Paginator

# Create your views here.
def index(request):

    all_posts = Post.objects.all()
    amount_posts = Post.objects.count()

    paginator = Paginator(all_posts, 3)
    page = request.GET.get('page')
    all_posts_page = paginator.get_page(page)

    context = {
        'all_posts': all_posts_page,
        'created_form': PostForm(),
        'amount_posts': amount_posts,
    }

    return render(request, 'article/index.html', context)


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    post = Post.objects.get(pk=post_id)
    update_form = PostForm(instance=post)
    context = {
        'post': post,
        'update_form': update_form
    }
    return render(request, 'article/detail.html', context)

def create_view(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('article:detail' , post_id=post.id)
        
@login_required
def delete_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id, author=request.user)
        post.delete()
        messages.success(request, 'Post deleted successfully')
    return redirect('article:index')

@login_required
def update_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id, author=request.user)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')
        else:
            messages.error(request, 'Error updating post')
        return redirect('article:detail', post_id=post.id)
    return redirect('article:index')