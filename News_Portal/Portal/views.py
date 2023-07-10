from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscription
from .filters import ProductFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Exists, OuterRef


class PostsList(Category, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('Portal.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'news'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('Portal.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'post'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('Portal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('Portal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('Portal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
