from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from store.models import ProductCategory


class Command(BaseCommand):
    help = "Generate fake product categories"

    def handle(self, *args, **kwargs):
        fake = Faker("fa_IR")

        for _ in range(10):
            title = fake.word()

            ProductCategory.objects.create(
                title=title,
                slug=slugify(title,allow_unicode=True)
            )

        self.stdout.write(
            self.style.SUCCESS("10 categories created successfully")
        )