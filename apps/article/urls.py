from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.detail, name='detail'),
    path('create/', views.create_view, name='create'),
    
    path('delete/<int:post_id>/', views.delete_view, name='delete'),    #google.com/blog/delete/1/
    path('update/<int:post_id>/', views.update_view, name='update'),    #google.com/blog/update/1/
]