from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
from django.contrib.auth.models import User
import os


# Dummy Data
'''posts = [
    {
        'author': 'coreyms',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018',
    },
    {
        'author': 'john doe',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018',
    }
]'''


class PostListView(ListView):
    model = Post
    template_name = 'blog1/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by  = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog1/user_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by  = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url ='/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    


def about(request):
    AWS_STORAGE_BUCKET_NAME = os.environ.get('MYBLOG_AWS_STORAGE_BUCKET_NAME')
    AWS_SECRET_ACCESS_KEY = os.environ.get('MYBLOG_AWS_SECRET_ACCESS_KEY')
    AWS_ACCESS_KEY_ID = os.environ.get('MYBLOG_AWS_ACCESS_KEY_ID')

    context = { AWS_STORAGE_BUCKET_NAME :'bucket_name',
                AWS_SECRET_ACCESS_KEY :'secret_key',
                AWS_ACCESS_KEY_ID : 'key_id'
               }
    return render(request, 'blog1/about.html', context)
