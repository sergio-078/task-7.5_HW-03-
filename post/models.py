from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


# создание модели Автора новости/статьи
class Author(models.Model):
    authorUser = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    # метод подсчёта рейтинга пользователя
    def update_rating(self):
        resultPost = self.post_set.aggregate(postRating=Sum('rating'))
        ratingPost = 0
        ratingPost += resultPost.get('postRating')

        resultComment = self.post_set.aggregate(commentRating=Sum('rating'))
        ratingComment = 0
        ratingComment += resultComment.get('commentRating')

        self.ratingAuthor = ratingPost*3 + ratingComment
        self.save()

    def __str__(self):
        return self.authorUser.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

# создание модели Категории новости/статьи (спорт, политика, образование и т. д.)
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название категории')
    discription = models.TextField(verbose_name='Описание категории')
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories', verbose_name='Подписчики', through='Subscriber')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# создание модели Новости/статьи, которые создают пользователи
class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    NOTIFICATION = 'NT'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
        (NOTIFICATION, 'Объявление'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE, verbose_name='Тип публикации')
    dateCreation = models.DateTimeField(default=timezone.now, verbose_name='Дата и время создания публикации')
    title = models.CharField(max_length=128, verbose_name='Заголовок публикации')
    text = models.TextField(verbose_name='Текст публикации')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг публикации')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор публикации')
    category = models.ManyToManyField(Category, verbose_name='Категория публикации')

    # метод лайков
    def like(self):
        self.rating += 1
        self.save()

    # метод дизлайков
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:29]} ...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-dateCreation',]
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


# создание модели Комментарии
class Comment(models.Model):
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    # метод лайков
    def like(self):
        self.rating += 1
        self.save()

    # метод дизлайков
    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions',)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscriptions',)
