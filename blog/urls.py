from django.urls import path, include
from .views import (
    BlogPostListView, BlogPostDetailView, AuthorListView, CommentCreateView, 
    AuthorDetailView, HomeView, custom_logout
)
from django.contrib.auth import views as auth_views  # Import Django's auth views
from .views import create_post, edit_post, delete_post

from .views import signup_view
app_name = "blog"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('blogs/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('bloggers/', AuthorListView.as_view(), name='author-list'),
    path('blogger/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('blog/<int:pk>/create/', CommentCreateView.as_view(), name='add-comment'),
    path('accounts/', include('django.contrib.auth.urls')),  # Includes login/logout URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('custom-logout/', custom_logout, name='custom-logout'),
    path('post/create/', create_post, name='create_post'),
    path('blog/<int:pk>/edit/', edit_post, name='edit-post'),
    path('blog/<int:pk>/delete/', delete_post, name='delete-post'),
    path("signup/", signup_view, name="signup"),
    
]
