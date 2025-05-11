# core/management/commands/seed_all.py

import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

# Import your models
from blog.models import Category, Blog, Comment
from testimonial.models import Testimonial
from blog.models import Objective, Skill, Role, Product

User = get_user_model()

class Command(BaseCommand):
    help = "Seed database with sample data for Users, Categories, Objectives, Skills, Roles, Products, Blogs, Comments, and Testimonials"

    def handle(self, *args, **options):
        fake = Faker()

        # 1) Create sample users
        self.stdout.write("Seeding users...")
        users = []
        for _ in range(10):
            email = fake.unique.email()
            username = fake.unique.user_name()
            user = User.objects.create_user(
                username=username,
                email=email,
                password="password123",
                phone=getattr(User, 'phone', '') and fake.phone_number()
            )
            users.append(user)

        # 2) Create categories
        self.stdout.write("Seeding categories...")
        category_names = ['ITSM', 'ITOM', 'ITBM', 'DevOps', 'Cloud']
        categories = []
        for name in category_names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)

        # 3) Create objectives, skills, roles, products
        self.stdout.write("Seeding objectives, skills, roles, and products...")
        objective_list = ['Learn Basics', 'Certification Prep', 'Advanced Tips', 'Project Deployment']
        skill_list = ['Python', 'Django', 'JavaScript', 'HTML', 'CSS', 'DevOps']
        role_list = ['Developer', 'Administrator', 'Architect', 'Consultant']
        product_list = ['ServiceNow', 'Salesforce', '.NET', 'WordPress']

        objectives = []
        for n in objective_list:
            obj, _ = Objective.objects.get_or_create(name=n)
            objectives.append(obj)
        skills = []
        for n in skill_list:
            sk, _ = Skill.objects.get_or_create(name=n)
            skills.append(sk)
        roles = []
        for n in role_list:
            r, _ = Role.objects.get_or_create(name=n)
            roles.append(r)
        products = []
        for n in product_list:
            p, _ = Product.objects.get_or_create(name=n)
            products.append(p)

        # 4) Create blogs
        self.stdout.write("Seeding blogs...")
        blogs = []
        for _ in range(20):
            title = fake.sentence(nb_words=6)
            slug = fake.unique.slug()
            blog = Blog.objects.create(
                title=title,
                slug=slug,
                category=random.choice(categories),
                content="\n\n".join(fake.paragraphs(nb=5))
            )
            # assign random filters
            blog.objectives.set(random.sample(objectives, k=2))
            blog.skills.set(random.sample(skills, k=3))
            blog.roles.set(random.sample(roles, k=2))
            blog.products.set(random.sample(products, k=1))
            blogs.append(blog)

        # 5) Create comments for each blog
        self.stdout.write("Seeding comments...")
        for blog in blogs:
            for _ in range(random.randint(1, 5)):
                Comment.objects.create(
                    blog=blog,
                    name=fake.name(),
                    email=fake.email(),
                    comment=fake.paragraph(nb_sentences=3)
                )

        # 6) Create testimonials
        self.stdout.write("Seeding testimonials...")
        for _ in range(10):
            Testimonial.objects.create(
                name=fake.name(),
                designation=fake.job(),
                content=fake.paragraph(nb_sentences=3),
                # If Testimonial has an image, ensure blank=True or set default
            )

        self.stdout.write(self.style.SUCCESS("✅ Database seeding complete!"))
