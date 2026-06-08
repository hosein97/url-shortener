from django.core.management.base import BaseCommand

from analytics.services import flush_clicks


class Command(BaseCommand):

    help = "Flush click counters from Redis into Postgres"

    def handle(self, *args, **options):

        flush_clicks()

        self.stdout.write(
            self.style.SUCCESS(
                "Click counters flushed."
            )
        )