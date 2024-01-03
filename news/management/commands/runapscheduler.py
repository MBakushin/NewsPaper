import logging
from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category

logger = logging.getLogger(__name__)


def daily_posts():
    #  Your job processing logic here...
    today = datetime.today()
    last_week = today - timedelta(days=7)
    all_daily_posts = Post.objects.filter(time_to_create__gte=last_week)
    categories = set(all_daily_posts.values_list('category__title', flat=True))

    for category in categories:
        if category:
            posts = all_daily_posts.filter(category__title=category)
            subscribers_email = list(Category.objects.get(title=category).subscribers.all().values_list('email', flat=True))
            html_context = render_to_string(
                'news/daily_posts_email.html',
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


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            daily_posts,
            trigger=CronTrigger(day_of_week="wed", hour="15", minute="19"),
            id="daily_posts",  # unique id
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'daily_posts'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
