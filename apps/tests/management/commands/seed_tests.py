import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.tests.models import Test


class Command(BaseCommand):
    help = "Seed database with 15,000 Tests"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Test seeding started..."))

        now = timezone.now()
        courses = []
        for i in range(1, 15001):
            start_at = now + timedelta(days=random.randint(-20, 20))
            end_at = start_at + timedelta(days=10)
            created_at = start_at - timedelta(days=10)

            courses.append(
                Test(
                    title=f"Test {i}",
                    start_at=start_at,
                    end_at=end_at,
                    created_at=created_at,
                )
            )

        # bulk insert
        Test.objects.bulk_create(courses, batch_size=1000)
        self.stdout.write(self.style.SUCCESS("Test Seeding finished!"))
