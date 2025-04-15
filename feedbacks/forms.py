from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["comments", "stars", "comments_like", "comments_dislike", "location"]

    def clean(self):
        cleaned_data = super().clean()
        comments_like = cleaned_data.get("comments_like")
        comments_dislike = cleaned_data.get("comments_dislike")

        if comments_like:
            cleaned_data["comments_dislike"] = 0
        elif comments_dislike:
            cleaned_data["comments_like"] = 0

        return cleaned_data

    def save(self, commit=True, user=None):
        feedback = super().save(commit=False)
        if user:
            feedback.user = user
        if commit:
            feedback.save()
        return feedback
