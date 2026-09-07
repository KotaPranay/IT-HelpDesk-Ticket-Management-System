from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name


class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Closed", "Closed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    assigned_to = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="assigned_tickets"
)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE
    )

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.message[:50]


class Attachment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE
    )

    file = models.FileField(upload_to="attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.file.name


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("Employee", "Employee"),
        ("Support Engineer", "Support Engineer"),
        ("Admin", "Admin"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )

    def _str_(self):
        return f"{self.user.username} - {self.role}"

class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.ticket.title} - {self.user.username}"    