# myapp/management/commands/delete_old_posts.py
from django.core.management.base import BaseCommand
from myapp.models import BlogPost
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
import datetime

class Command(BaseCommand):
    help = 'Delete all blog posts older than a certain date'

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, help='Date in YYYY-MM-DD format. Delete posts older than this date.')

    def handle(self, *args, **kwargs):
        date_str = kwargs['date']
        date = parse_date(date_str)
        
        if date is None:
            self.stderr.write(self.style.ERROR('Invalid date format. Use YYYY-MM-DD.'))
            return

        # Ensure the date is timezone-aware
        date = make_aware(datetime.datetime.combine(date, datetime.datetime.min.time()))

        # Query and delete posts older than the given date
        old_posts = BlogPost.objects.filter(created_at__lt=date)
        count = old_posts.count()
        old_posts.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} blog post(s) older than {date_str}.'))
