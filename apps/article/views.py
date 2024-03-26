from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm

from django.http import JsonResponse

from django.contrib import messages

from django.core.paginator import Paginator

# Create your views here.
def index(request):
    all_posts = Post.objects.all()
    amount_posts = Post.objects.count()

    # for post in all_posts: # перебирання всіх постів
    #     for s in post.comments.all(): # перебирання коментарів кожного поста 
    #         if s.author_id == request.user.id: # і перевірка на ідентичність id юзера та автора коментарів 
    #             print(1111)

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
        'update_form': update_form,
    }
    return render(request, 'article/detail.html', context)


def create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post was created successfully')
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


@login_required
def like_view(request, post_id):
    if request.method == 'GET':
        user_dislike = None
        post = get_object_or_404(Post, pk=post_id)
        # print(post.like.all())
        if request.user in post.like.all():
            post.like.remove(request.user)
            user_like = False
        else:
            post.like.add(request.user)
            user_like = True
            if request.user in post.dislike.all():
                post.dislike.remove(request.user)
                user_dislike = False
        return JsonResponse( {'like_count': post.like.count(), 'user_like': user_like, 'user_dislike': user_dislike, 'dislike_count': post.dislike.count()} )


@login_required
def dislike_view(request, post_id):
    if request.method == 'GET':
        user_like = None
        post = get_object_or_404(Post, pk=post_id)
        # print(post.dislike.all())
        if request.user in post.dislike.all():
            post.dislike.remove(request.user)
            user_dislike = False
        else:
            post.dislike.add(request.user)
            user_dislike = True
            if request.user in post.like.all():
                post.like.remove(request.user)
                user_like = False
        return JsonResponse( {'dislike_count': post.dislike.count(), 'user_dislike': user_dislike, 'user_like': user_like, 'like_count': post.like.count()} )


@login_required
def like_comment_view(request, comment_id):
    if request.method == 'GET':
        user_dislike = None
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user in comment.like.all():
            comment.like.remove(request.user)
            user_like = False
        else:
            comment.like.add(request.user)
            user_like = True
            if request.user in comment.dislike.all():
                comment.dislike.remove(request.user)
                user_dislike = False
        return JsonResponse( {'like_count': comment.like.count(), 'user_like': user_like, 'user_dislike': user_dislike, 'dislike_count': comment.dislike.count()} )


@login_required
def dislike_comment_view(request, comment_id):
    if request.method == 'GET':
        user_like = None
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user in comment.dislike.all():
            comment.dislike.remove(request.user)
            user_dislike = False
        else:
            comment.dislike.add(request.user)
            user_dislike = True
            if request.user in comment.like.all():
                comment.like.remove(request.user)
                user_like = False
        return JsonResponse( {'dislike_count': comment.dislike.count(), 'user_dislike': user_dislike, 'user_like': user_like, 'like_count': comment.like.count()} )


@login_required
def comment_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=form.cleaned_data['content']
            )
            comment.save()
            messages.success(request, 'Comment created successfully')
        else:
            messages.error(request, 'Error creating comment')
    return redirect('article:detail', post_id=post_id)
