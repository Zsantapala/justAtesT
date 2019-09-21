from django.urls import path
from . import views
urlpatterns =[
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit_page/', views.edit_page, name='edit_page'),
    path('article/<int:article_id>', views.article, name='article'),
    path('edit_article/<int:article_id>', views.edit_article, name='edit_article'),
    path('p/<int:page>', views.arti_list, name='article_list'),
]