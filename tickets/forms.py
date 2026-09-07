from django import forms
from .models import Ticket, Comment, Attachment


# class TicketForm(forms.ModelForm):
#     class Meta:
#         model = Ticket
#         fields = [
#             "title",
#             "category",
#             "priority",
#             "description",
#         ]


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            "title",
            "category",
            "priority",
            "description",
        ]

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if not title:
            raise forms.ValidationError(
                "Ticket title is required."
            )

        if len(title.strip()) < 5:
            raise forms.ValidationError(
                "Ticket title must contain at least 5 characters."
            )

        return title.strip()

    def clean_description(self):
        description = self.cleaned_data.get("description")

        if not description:
            raise forms.ValidationError(
                "Ticket description is required."
            )

        if len(description.strip()) < 10:
            raise forms.ValidationError(
                "Ticket description must contain at least 10 characters."
            )

        return description.strip()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]

        widgets = {
            "comment": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Write your comment here..."
            })
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ["file"]