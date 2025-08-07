from django.conf import settings
from django.core.management.base import BaseCommand
from mart.loader.registry import get_loader_for

class Command(BaseCommand):
    help = 'Load DataMart model'

    def add_arguments(self, parser):
        parser.add_argument('model', help="e.g. 'mart.partner'")
        parser.add_argument(
            '--countries', type=lambda s: s.split(','),
            help='Comma-separated tenant schemas'
        )
        parser.add_argument(
            '--workers', type=int,
            default=settings.ETL_PARALLEL_WORKERS,
            help='Parallel loaders count'
        )
        parser.add_argument(
            '--ignore-errors', action='store_true',
            help='Continue on errors'
        )
        parser.add_argument(
            '--verbosity', type=int, default=1,
            help='Verbosity'
        )

    def handle(self, *args, **opts):
        loader = get_loader_for(opts['model'])
        results = loader.load(
            countries=opts.get('countries'),
            workers=opts.get('workers'),
            ignore_errors=opts.get('ignore_errors'),
            verbosity=opts.get('verbosity'),
            stdout=self.stdout
        )
        self.stdout.write(f"Results: {results}")