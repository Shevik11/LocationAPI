from django.urls import path
from . import views

urlpatterns = [
    path(
        "feedback/",
        views.FeedbacksListCreateAPIView.as_view(),
        name="feedback-list-create",
    ),
    path(
        "feedback/<int:pk>/",
        views.FeedbackRetrieveUpdateDestroyAPIView.as_view(),
        name="feedbacks-retrieve-update-destroy",
    ),
]
