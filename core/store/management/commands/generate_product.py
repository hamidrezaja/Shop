from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
import random

from store.models import ProductModel, ProductCategory,ProductStatusType
from accounts.models import CustomUser,UserType
from pathlib import Path
from django.core.files import File
 
BASE_DIR = Path(__file__).resolve().parent



class Command(BaseCommand):
    help = "Generate fake products"

    def handle(self, *args, **kwargs):
        fake = Faker("fa_IR")

        users = list(CustomUser.objects.filter(type=UserType.admin.value))
        categories = list(ProductCategory.objects.all())
        # List of images
        image_list = [
            "./images/img1.jpg",
            "./images/img2.jpg",
            "./images/img3.jpg",
            "./images/img4.jpg",
            "./images/img5.jpg",
            "./images/img6.jpg",
            "./images/img7.jpg",
            "./images/img8.jpg",
            # Add more image filenames as needed
        ]

        if not users:
            self.stdout.write(self.style.ERROR("No users found"))
            return

        if not categories:
            self.stdout.write(self.style.ERROR("No categories found"))
            return

        for _ in range(10):
            title = fake.sentence(nb_words=3)
            selected_image=random.choice(image_list,)
            image_obj=File(file=open(BASE_DIR / selected_image,"rb"),name=Path(selected_image).name)
            product = ProductModel.objects.create(
                user=random.choice(users),
                title=title,
                slug=slugify(f"{title}-{fake.unique.random_int()}"),
                description=fake.text(max_nb_chars=500),
                brief_description=fake.text(max_nb_chars=100),
                stock=random.randint(1, 100),
                price=random.randint(100000, 5000000),
                discount_percent=random.randint(0, 50),
                status=random.choice(ProductStatusType.choices)[0],
                image=image_obj
                
            )

            selected_categories = random.sample(
                categories,
                random.randint(1, min(3, len(categories)))
            )

            product.category.add(*selected_categories)

        self.stdout.write(
            self.style.SUCCESS("10 fake products created successfully")
        )