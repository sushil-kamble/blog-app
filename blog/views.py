from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from .models import Post
from django.contrib import messages


# Create your views here.
def index(request):
    prams = {
        'posts': Post.objects.all()
    }
    return render(request, 'home.html', prams)


class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'  # object_list
    ordering = ['-date_posted']
    paginate_by = 3


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.INFO, f'Your Post is Posted')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.INFO, f'Your Post is Updated')
        print(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
