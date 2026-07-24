from django.core.management.base import BaseCommand

from shortener.consumer import start_consumer


class Command(BaseCommand):

    help = "Start RabbitMQ click counters consumer"

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.SUCCESS(
                "Starting click counters consumer..."
            )
        )

        start_consumer()