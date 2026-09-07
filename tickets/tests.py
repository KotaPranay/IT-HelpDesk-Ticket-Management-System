from django.test import TestCase
from django.urls import reverse


class LoginPageTest(TestCase):

    def test_login_page_loads(self):
        response = self.client.get(
            reverse("login")
        )

        self.assertEqual(
            response.status_code,
            200
        )


class DashboardPageTest(TestCase):

    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            302
        )

from django.contrib.auth.models import User
from .models import Ticket, Category


class TicketModelTest(TestCase):

    def test_ticket_can_be_created(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        category = Category.objects.create(
            name="Test Category"
        )

        ticket = Ticket.objects.create(
            title="Test Ticket",
            description="This is a test ticket description.",
            category=category,
            priority="High",
            created_by=user
        )

        self.assertEqual(
            ticket.title,
            "Test Ticket"
        )


class TicketCreationIntegrationTest(TestCase):
    def test_user_can_create_ticket(self):
        user = User.objects.create_user(
            username="employee_test",
            password="testpass123"
        )

        category = Category.objects.create(
            name="Hardware"
        )

        self.client.login(
            username="employee_test",
            password="testpass123"
        )

        response = self.client.post(
            reverse("create_ticket"),
            {
                "title": "Laptop Not Working",
                "description": "My laptop is not starting properly.",
                "category": category.id,
                "priority": "High",
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Ticket.objects.filter(
                title="Laptop Not Working",
                created_by=user
            ).exists()
        )        