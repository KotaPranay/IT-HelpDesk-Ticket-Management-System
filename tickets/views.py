from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.core.mail import send_mail

from .forms import TicketForm, CommentForm, AttachmentForm
from .models import Ticket, Comment, Attachment


# =========================
# USER LOGIN
# =========================

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid Username or Password"
            }
        )

    return render(request, "login.html")


# =========================
# EMAIL NOTIFICATION
# =========================

def send_notification_email(user, subject, message):
    if user and user.email:
        send_mail(
            subject,
            message,
            "helpdesk@example.com",
            [user.email],
            fail_silently=True,
        )


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):
    profile = request.user.userprofile

    # =========================
    # ADMIN DASHBOARD
    # =========================

    if profile.role == "Admin":
        tickets = Ticket.objects.all()

        total_tickets = tickets.count()

        open_tickets = tickets.filter(
            status="Open"
        ).count()

        in_progress_tickets = tickets.filter(
            status="In Progress"
        ).count()

        closed_tickets = tickets.filter(
            status="Closed"
        ).count()

        high_priority_tickets = tickets.filter(
            priority="High"
        ).count()

        medium_priority_tickets = tickets.filter(
            priority="Medium"
        ).count()

        low_priority_tickets = tickets.filter(
            priority="Low"
        ).count()

        return render(
            request,
            "admin_dashboard.html",
            {
                "tickets": tickets,
                "total_tickets": total_tickets,
                "open_tickets": open_tickets,
                "in_progress_tickets": in_progress_tickets,
                "closed_tickets": closed_tickets,
                "high_priority_tickets": high_priority_tickets,
                "medium_priority_tickets": medium_priority_tickets,
                "low_priority_tickets": low_priority_tickets,
            }
        )

    # =========================
    # SUPPORT ENGINEER DASHBOARD
    # =========================

    elif profile.role == "Support Engineer":
        tickets = Ticket.objects.filter(
            assigned_to=request.user
        )

        total_tickets = tickets.count()

        open_tickets = tickets.filter(
            status="Open"
        ).count()

        in_progress_tickets = tickets.filter(
            status="In Progress"
        ).count()

        closed_tickets = tickets.filter(
            status="Closed"
        ).count()

        high_priority_tickets = tickets.filter(
            priority="High"
        ).count()

        medium_priority_tickets = tickets.filter(
            priority="Medium"
        ).count()

        low_priority_tickets = tickets.filter(
            priority="Low"
        ).count()

        return render(
            request,
            "engineer_dashboard.html",
            {
                "tickets": tickets,
                "total_tickets": total_tickets,
                "open_tickets": open_tickets,
                "in_progress_tickets": in_progress_tickets,
                "closed_tickets": closed_tickets,
                "high_priority_tickets": high_priority_tickets,
                "medium_priority_tickets": medium_priority_tickets,
                "low_priority_tickets": low_priority_tickets,
            }
        )

    # =========================
    # EMPLOYEE DASHBOARD
    # =========================

    else:
        tickets = Ticket.objects.filter(
            created_by=request.user
        )

        total_tickets = tickets.count()

        open_tickets = tickets.filter(
            status="Open"
        ).count()

        in_progress_tickets = tickets.filter(
            status="In Progress"
        ).count()

        closed_tickets = tickets.filter(
            status="Closed"
        ).count()

        high_priority_tickets = tickets.filter(
            priority="High"
        ).count()

        medium_priority_tickets = tickets.filter(
            priority="Medium"
        ).count()

        low_priority_tickets = tickets.filter(
            priority="Low"
        ).count()

        return render(
            request,
            "employee_dashboard.html",
            {
                "tickets": tickets,
                "total_tickets": total_tickets,
                "open_tickets": open_tickets,
                "in_progress_tickets": in_progress_tickets,
                "closed_tickets": closed_tickets,
                "high_priority_tickets": high_priority_tickets,
                "medium_priority_tickets": medium_priority_tickets,
                "low_priority_tickets": low_priority_tickets,
            }
        )


# =========================
# USER LOGOUT
# =========================

def user_logout(request):
    logout(request)
    return redirect("/login/")


# =========================
# CREATE TICKET
# =========================

@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()

            return redirect("/dashboard/")

    else:
        form = TicketForm()

    return render(
        request,
        "create_ticket.html",
        {
            "form": form
        }
    )


# =========================
# VIEW TICKETS
# =========================

@login_required
def view_tickets(request):
    tickets = Ticket.objects.all()

    return render(
        request,
        "view_tickets.html",
        {
            "tickets": tickets
        }
    )


# =========================
# ASSIGN TICKET
# =========================

@login_required
def assign_ticket(request, ticket_id):

    # Only Admin can assign tickets
    if not request.user.is_superuser:
        messages.error(
            request,
            "You are not authorized to assign tickets."
        )
        return redirect("/dashboard/")

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    engineers = User.objects.all()

    if request.method == "POST":

        engineer_id = request.POST["engineer"]

        engineer = User.objects.get(
            id=engineer_id
        )

        ticket.assigned_to = engineer
        ticket.save()

        # Send assignment notification
        send_notification_email(
            engineer,
            "New Ticket Assigned",
            f"You have been assigned a new ticket: {ticket.title}"
        )

        messages.success(
            request,
            f"Ticket '{ticket.title}' assigned successfully to {engineer.username}."
        )

        return redirect("/dashboard/")

    return render(
        request,
        "assign_ticket.html",
        {
            "ticket": ticket,
            "engineers": engineers,
        }
    )


# =========================
# UPDATE TICKET STATUS
# =========================

@login_required
def update_status(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    if request.method == "POST":
        new_status = request.POST["status"]

        ticket.status = new_status
        ticket.save()

        # Send status update notification
        send_notification_email(
            ticket.created_by,
            "Ticket Status Updated",
            f"Your ticket '{ticket.title}' status has been changed to {new_status}."
        )

        messages.success(
            request,
            f"Ticket '{ticket.title}' status updated to {new_status}."
        )

        return redirect("/dashboard/")

    return render(
        request,
        "update_status.html",
        {
            "ticket": ticket,
        }
    )


# =========================
# TICKET DETAILS
# =========================

@login_required
def ticket_details(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )

    comments = Comment.objects.filter(
        ticket=ticket
    ).order_by("created_at")

    attachments = Attachment.objects.filter(
        ticket=ticket
    ).order_by("-uploaded_at")

    comment_form = CommentForm()
    attachment_form = AttachmentForm()

    if request.method == "POST":

        # Add Comment
        if "comment_submit" in request.POST:
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(
                    commit=False
                )

                comment.ticket = ticket
                comment.user = request.user
                comment.save()

                return redirect(
                    "ticket_details",
                    ticket_id=ticket.id
                )

        # Upload Attachment
        elif "attachment_submit" in request.POST:
            attachment_form = AttachmentForm(
                request.POST,
                request.FILES
            )

            if attachment_form.is_valid():
                attachment = attachment_form.save(
                    commit=False
                )

                attachment.ticket = ticket
                attachment.save()

                return redirect(
                    "ticket_details",
                    ticket_id=ticket.id
                )

    return render(
        request,
        "ticket_details.html",
        {
            "ticket": ticket,
            "comments": comments,
            "attachments": attachments,
            "comment_form": comment_form,
            "attachment_form": attachment_form,
        }
    )


# =========================
# DELETE ATTACHMENT
# =========================

@login_required
def delete_attachment(request, attachment_id):
    attachment = get_object_or_404(
        Attachment,
        id=attachment_id
    )

    ticket_id = attachment.ticket.id

    if request.method == "POST":
        attachment.file.delete()
        attachment.delete()

        return redirect(
            "ticket_details",
            ticket_id=ticket_id
        )

    return redirect(
        "ticket_details",
        ticket_id=ticket_id
    )


# =========================
# REPORTS
# =========================

@login_required
def reports(request):
    tickets = Ticket.objects.all()

    category_reports = (
        Ticket.objects
        .values("category__name")
        .annotate(
            ticket_count=Count("id")
        )
        .order_by("category__name")
    )

    total_tickets = tickets.count()

    open_tickets = tickets.filter(
        status="Open"
    ).count()

    in_progress_tickets = tickets.filter(
        status="In Progress"
    ).count()

    closed_tickets = tickets.filter(
        status="Closed"
    ).count()

    high_priority = tickets.filter(
        priority="High"
    ).count()

    medium_priority = tickets.filter(
        priority="Medium"
    ).count()

    low_priority = tickets.filter(
        priority="Low"
    ).count()

    return render(
        request,
        "reports.html",
        {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "closed_tickets": closed_tickets,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority,
            "category_reports": category_reports,
        }
    )