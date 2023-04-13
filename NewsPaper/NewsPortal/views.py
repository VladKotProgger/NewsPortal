from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.

from datetime import datetime

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import ArticleNewsForm
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(CreateView):
    form_class = ArticleNewsForm
    model = Post
    template_name = 'post_create_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_news = 'NOV'
        return super().form_valid(form)


class NewsEdit(UpdateView):
    form_class = ArticleNewsForm
    model = Post
    template_name = 'post_create_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.article_news == 'STA':
            return HttpResponse('Такой статьи не существует')
        post.save()
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = ArticleNewsForm
    model = Post
    template_name = 'article_create_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_news = 'STA'
        return super().form_valid(form)


class ArticleEdit(UpdateView):
    form_class = ArticleNewsForm
    model = Post
    template_name = 'article_create_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.article_news == 'NOV':
            return HttpResponse('Такой новости не существует')
        post.save()
        return super().form_valid(form)


def PostDelete(request, pk):
    article = Post.objects.get(id=pk)
    article.delete()
    return HttpResponseRedirect(reverse('post_list'))
