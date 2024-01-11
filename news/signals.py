from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string

from config import settings
from news.models import PostCategory, Post
from news.tasks import send_notifications


@receiver(pre_save, sender=Post)
def check_post_per_day(sender, instance, **kwargs):
    author = instance.author
    today_posts = Post.get_author_today_posts(author)

    if len(today_posts) >= 4:
        raise Exception(f'More than 3 posts per day by {author}')


# def send_notifications(pk, header, preview, subscribers_email):
#     html_context = render_to_string(
#         'news/post_created_email.html',
#         {
#             'header': header,
#             'text': preview,
#             'link': f'{settings.SITE_URL}/news/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=header,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers_email,
#     )
#
#     msg.attach_alternative(html_context, 'text/html')
#     msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers = list()

        for category in categories:
            subscribers += category.subscribers.all()

        subscribers_email = [s.email for s in subscribers]

        send_notifications.delay(instance.pk, instance.header, instance.preview(),
                           subscribers_email)
