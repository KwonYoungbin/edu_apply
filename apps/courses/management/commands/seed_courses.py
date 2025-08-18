import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.courses.models import Course, Tag


class Command(BaseCommand):
    help = "Seed database with 15,000 Courses with random Tags"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Course seeding started..."))

        tags = list(Tag.objects.all())
        if not tags:
            self.stdout.write(self.style.ERROR("먼저 loaddata로 Tag를 불러와야 합니다."))
            return

        now = timezone.now()
        courses = []
        for i in range(1, 15001):
            start_at = now + timedelta(days=random.randint(-20, 20))
            end_at = start_at + timedelta(days=10)
            created_at = start_at - timedelta(days=10)

            courses.append(
                Course(
                    title=f"Course {i}",
                    start_at=start_at,
                    end_at=end_at,
                    created_at=created_at,
                )
            )

        # bulk insert
        Course.objects.bulk_create(courses, batch_size=1000)
        self.stdout.write(self.style.SUCCESS("Courses 생성 완료"))

        # ManyToMany 매핑 (랜덤 1~3개 태그)
        all_courses = Course.objects.all()
        for course in all_courses:
            if not course.tags.exists():
                course.tags.set(random.sample(tags, random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS("Course Seeding finished!"))
