from django.core.management.base import BaseCommand, CommandError

from news.models import Post, Category


class Command(BaseCommand):
    help = 'Delete all posts in chosen category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Are you sure you want to delete all posts in this category {options["category"]}? (y/n)')

        if answer != 'y':
            self.stdout.write(self.style.ERROR('Aborting'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted all posts in category {options["category"]}!'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Category {options["category"]} does not exist!'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No posts in category {options["category"]}!'))
