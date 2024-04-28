import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from newsportal import settings
from post.models import Post, Category


@shared_task
def email_weekly_post_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week).order_by('-dateCreation')
    categories = set(posts.values_list('category__name', flat=True))
    subscribers_emails = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    for subscriber in subscribers_emails:
        subject = 'Статьи за неделю!!!',
        text_content = render_to_string(
            'post/email_weekly_post.html',
            {
                'username': subscriber.username,
                'link': settings.SITE_URL,
                'posts': posts,
            }
        )
        html_content = render_to_string(
            'post/email_weekly_post.html',
            {
                'link': settings.SITE_URL,
                'posts': posts,
            }
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [subscriber])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def email_new_post_task(preview, pk, title, subscribers):
    html_content = render_to_string(
    'post/email_new_post.html',
    {
        'text': preview,
        'link': f'{settings.SITE_URL}/post/{pk}'}
    )

    msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
