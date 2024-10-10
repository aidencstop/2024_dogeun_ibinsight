from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_list, name='forum_list'),  # This matches http://127.0.0.1:8000/forum/
    # path('<int:pk>/', views.forum_detail, name='forum_detail'),  # Matches specific forum details
    path('new/', views.create_post, name='create_post'),  # Matches new thread creation
    # path('posts/', views.post_list, name='post_list'),  # List of posts
    path('post/<int:id>/', views.post_detail, name='post_detail'),  # Detail page for a post

]
