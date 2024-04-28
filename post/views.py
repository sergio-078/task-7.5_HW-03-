from django.shortcuts import redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin # , LoginRequiredMixin
# from django.urls import reverse_lazy
from django.views.generic import (DetailView, ListView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
# from django.conf import settings

from .models import Post, Category, Subscriber
from .filters import PostFilter
from .forms import PostForm, EditForm


class PostDetail(DetailView):
    # Модель по которой мы хотим получать информацию по отдельной статье
    model = Post
    # Используем шаблон — post_detail.html
    template_name = "post/post_detail.html"
    # Название объекта, в котором будет выбранная пользователем статья
    context_object_name = "postdetail"


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/home.html'
    context_object_name = 'postlist'    # название класса, по которому будем обращаться в коде
    paginate_by = 10    # количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'post/list_news.html'
    context_object_name = 'newslist'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ArticleList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'post/list_article.html'
    context_object_name = 'articlelist'
    paginate_by = 10


class NotificationList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'post/list_notification.html'
    context_object_name = 'notificationlist'
    paginate_by = 10


class PostCreate(PermissionRequiredMixin, CreateView):
    # запрос на наличие указанных нами прав
    permission_required = ('post.add_post',)
    # raise_exception = True    # аутентификация
    # Указываем нашу разработанную форму
    form_class = PostForm
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post/post_create.html'


class PostSearch(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filterset_class = PostFilter
    ordering = '-dateCreation'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostHome(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/home.html'
    context_object_name = 'postlist'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('post.change_post',)
    # raise_exception = True
    form_class = EditForm
    model = Post
    template_name = 'post/post_edit.html'

    def form_valid(self, form):
        return super().form_valid(form)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('post.delete_post',)
    # raise_exception = True
    model = Post
    template_name = 'post/post_delete.html'
    context_object_name = 'postdelete'

    def form_valid(self, form):
        self.object.delete()
        return redirect('portal_home')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        # user = request.user
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'post/subscriptions.html',
        # 'account/personal_cabinet.html',
        {'categories': categories_with_subscriptions},
    )
