from django.core.management.base import BaseCommand

from analytics.consumer import start_consumer


class Command(BaseCommand):

    help = "Start RabbitMQ click events consumer"

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.SUCCESS(
                "Starting click events consumer..."
            )
        )

        start_consumer()