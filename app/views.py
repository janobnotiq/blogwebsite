from multiprocessing import get_context
from typing import Any, Dict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Comment


def mainpage(request):
    posts = Post.objects.all()
    ctx = {'posts': posts}
    return render(request, template_name='app/index.html', context=ctx)


class PostListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'app/posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class UserPostListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'app/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def post_detail(request,pk):
    post = get_object_or_404(Post,id=pk)
    total_likes = post.total_likes
    comments = Comment.objects.filter(post__id=pk)

    return render(request,"app/post_detail.html",{"post":post,"total_likes":total_likes,"comments":comments})


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
    success_url = '/posts/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def like_view(request,pk):
    post = get_object_or_404(Post,id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('posts'))


def most_viewed(request):
    posts = Post.objects.filter(likes__gt=1)

    return render(request,"app/popular_posts.html",{"posts":posts})

def latest(request):
    posts = Post.objects.order_by("-date_posted")[:4]

    return render(request,"app/latest_posts.html",{"posts":posts})