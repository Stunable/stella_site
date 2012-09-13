from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = ""

    def handle_noargs(self, **options):
        import os
        os.system('cd apps;scrapy crawl shopbop')

        