from django.shortcuts import render, get_object_or_404, redirect

from .models import Post
from .forms import PostForm

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
    
    context = {
        'post': post
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