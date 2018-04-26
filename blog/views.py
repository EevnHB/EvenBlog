import markdown#markdown模块可以把文字转化成html格式输出到网页上
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from comments.forms import commentForm
from .models import Post, Category

# Create your views here.
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

class ArchivesView(IndexView):
    def get_requeryset(self):
        year = self.kwargs.year
        month = self.kwargs.month
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)

class CategoryView(IndexView):
    def get_requeryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_requeryset().filter(category=cate)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = commentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


