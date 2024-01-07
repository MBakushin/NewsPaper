from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from config import settings
from news.models import Category, Post


@shared_task
def send_notifications(pk, header, preview, subscribers_email):
    html_context = render_to_string(
        'news/post_created_email.html',
        {
            'header': header,
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@shared_task
def weekly_posts():
    #  Your job processing logic here...
    today = datetime.today()
    last_week = today - timedelta(days=7)
    all_weekly_posts = Post.objects.filter(time_to_create__gte=last_week)
    categories = set(all_weekly_posts.values_list('category__title', flat=True))

    for category in categories:
        if category:
            posts = all_weekly_posts.filter(category__title=category)
            subscribers_email = list(Category.objects.get(title=category).subscribers.all().values_list('email', flat=True))
            html_context = render_to_string(
                'news/weekly_posts_email.html',
                {
                    'link': settings.SITE_URL,
                    'posts': posts,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f"Новые посты в категории {category}",
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=subscribers_email,
            )

            msg.attach_alternative(html_context, 'text/html')
            msg.send()
