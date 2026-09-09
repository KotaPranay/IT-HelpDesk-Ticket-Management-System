import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a deployment admin user if one does not already exist."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        if not username or not password:
            self.stdout.write(
                "Admin environment variables not set; skipping."
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS("Deployment admin user created.")
            )
        else:
            self.stdout.write(
                "Deployment admin user already exists; no changes made."
            )