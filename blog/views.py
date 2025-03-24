from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404,redirect,render,reverse
from .models import BlogPost, Author, Comment
from .forms import CommentForm  # Ensure you have a CommentForm defined in forms.py
from django.views.generic import ListView
from .models import BlogPost  # Import your model

class HomeView(ListView):
    model = BlogPost  # Specify the model
    template_name = 'blog/home.html'
    context_object_name = 'posts'  # Optional: Custom context name

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 5  # Show 5 posts per page

    def get_queryset(self):
        return BlogPost.objects.all().order_by('-post_date')  # Sort by newest first

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(blog=self.object).order_by('created_at')  # Fetch comments sorted by oldest first
        return context

class AuthorListView(ListView):
    model = Author
    template_name = 'blog/author_list.html'
    context_object_name = 'authors'

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'blog/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_posts'] = BlogPost.objects.filter(author=self.object).order_by('-post_date')  # Fetch blog posts by the author
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        form.instance.blog = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
        form.instance.author = self.request.user.author  # Assuming a OneToOne relationship with User
        form.save()
        return redirect('blog:blog-detail', pk=self.kwargs['pk'])

    def get_login_url(self):
        return '/accounts/login/' 

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    """Logs out the user and redirects to the home page."""
    logout(request)
    return redirect('blog:home')  
# ... existing code ...
from django.shortcuts import redirect, get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm



def create_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                post.author = Author.objects.get(user=request.user)  # Get the Author instance
                post.save()
                return redirect("blog:blog-list")  # Redirect after successful creation
            except Author.DoesNotExist:
                return render(request, "blog/error.html", {"message": "No Author profile found for this user."})
    else:
        form = BlogPostForm()
    return render(request, "blog/create_post.html", {"form": form})





def edit_post(request, pk):
    post = get_object_or_404(BlogPost, id=pk, author=request.user.author)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('blog:blog-list'))  # ✅ Correct redirect
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form})

def delete_post(request, pk):  # Change post_id to pk
    post = get_object_or_404(BlogPost, id=pk, author=request.user.author)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:blog-list')
    return render(request, 'blog/confirm_delete.html', {'post': post})

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Author

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create User
            Author.objects.create(user=user, bio="New author bio")  # Create Author Profile
            return redirect("blog:login")  # Redirect to login after signup
    else:
        form = UserCreationForm()
    return render(request, "blog/signup.html", {"form": form})
