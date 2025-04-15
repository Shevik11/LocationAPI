from django.urls import path, include
from . import views


urlpatterns = [
    path(
        "locations/",
        views.LocationsListCreateAPIView.as_view(),
        name="locations-list-create",
    ),
    path(
        "locations/<int:pk>/",
        views.LocationsRetrieveUpdateDestroyAPIView.as_view(),
        name="locations-retrieve-update-destroy",
    ),
    path(
        "detail-location/<int:location_id>/",
        views.DetailLocationAPIView.as_view(),
        name="location-detail",
    ),
    path(
        "filter-rating/<int:pk>/",
        views.FilterFeedbacksByRateAPIView.as_view(),
        name="filter-rating",
    ),
    path(
        "filter-category/",
        views.FilterLocationsByCategoryAPIView.as_view(),
        name="filter-category",
    ),
    path("save_data/", views.SaveDataAPIView.as_view(), name="save-data"),
]
