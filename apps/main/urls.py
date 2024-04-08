from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('lol/', views.lol, name='lol'),

]