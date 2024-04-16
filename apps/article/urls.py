from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.detail, name='detail'),
    path('create_post/', views.create_post_view, name='create-post'),
    path('create_post/create', views.create_view, name='create'),

    path('delete/<int:post_id>/', views.delete_view, name='delete'),    #google.com/blog/delete/1/
    path('update/<int:post_id>/', views.update_view, name='update'),    #google.com/blog/update/1/
    path('like/<int:post_id>', views.like_view, name='like'),    #google.com/blog/like/1/
    path('dislike/<int:post_id>', views.dislike_view, name='dislike'),    #google.com/blog/dislike/1/

    path('post/<int:post_id>/comment/', views.comment_view, name='comment'),    #google.com/blog/1/comment/
    path('post/like_comment/<int:comment_id>', views.like_comment_view, name='like_comment'),    #google.com/blog/like_comment/
    path('post/dislike_comment/<int:comment_id>', views.dislike_comment_view, name='dislike_comment'),    #google.com/blog/like_comment/
]