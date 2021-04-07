from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import *
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


def like(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def category_list(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'blog/category_list.html', {'cat_menu_list': cat_menu_list})


def category(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'blog/categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})


class PostListView(ListView):  # List of all Posts
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    cats = Category.objects.all()

    # def get_context_data(self, *args, **kwargs):
    #     cat_menu = Category.objects.all()
    #     context = super(PostListView, self).get_context_data(*args, **kwargs)
    #     context["cat_menu"] = cat_menu
    #     return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):  # Details of a Post
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class PostCreateView(LoginRequiredMixin, CreateView):  # Create a new Post
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author of the post
        return super().form_valid(form)


class AddCategoryView(CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'blog/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        category = self.get_object()
        if self.request.user:
            return True
        return False


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # Update Posts
    model = Post
    form_class = PostForm
    template_name = 'blog/update_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  # Each user can only update their own posts
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
