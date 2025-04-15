from .models import Locations
from .utils import calculate_average_rating
import pandas as pd
from django.http import HttpResponse
from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer
from .serializers import LocationsSerializer
from rest_framework import viewsets, status, response, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class LocationsListCreateAPIView(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer

    def get_queryset(self):
        queryset = Locations.objects.all()
        name_query = self.request.query_params.get("name")
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)
        return queryset


class LocationsRetrieveUpdateDestroyAPIView(
    LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        instance.average_rating = calculate_average_rating(instance.id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Feedback.objects.filter(location=instance).delete()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class DetailLocationAPIView(LoginRequiredMixin, APIView):

    def get(self, request, location_id):
        location = Locations.objects.get(id=location_id)
        feedbacks = Feedback.objects.filter(location=location)
        average_rating = calculate_average_rating(location_id)
        location_data = LocationsSerializer(location).data
        feedbacks_data = FeedbackSerializer(feedbacks, many=True).data
        return response.Response(
            {
                "location": location_data,
                "feedbacks": feedbacks_data,
                "average_rating": average_rating,
            },
            status=status.HTTP_200_OK,
        )


class FilterFeedbacksByRateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        feedbacks = Feedback.objects.filter(stars__gte=pk)  # Отримуємо всі відгуки
        serializer = FeedbackSerializer(feedbacks, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class FilterLocationsByCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = request.query_params.get("category")

        if not category:
            return response.Response(
                {"error": "Параметр 'category' є обов'язковим"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        locations = Locations.objects.filter(category__iexact=category)
        serializer = LocationsSerializer(locations, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class SaveDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locations = Locations.objects.all().values("name", "average_rating", "category")
        locations_df = pd.DataFrame(locations)

        # Експорт даних для Feedback
        feedbacks = Feedback.objects.all().values(
            "user__username",
            "location__name",
            "comments",
            "comments_like",
            "comments_dislike",
            "stars",
        )
        feedbacks_df = pd.DataFrame(feedbacks)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="data_export.csv"'

        locations_df.to_csv("data1.csv", sep=";", index=False)
        feedbacks_df.to_csv("data2.csv", sep=";", index=False)

        return HttpResponse("save successfully", status=status.HTTP_200_OK)


#
# class LocationCreateView(LoginRequiredMixin, CreateView):
#     model = Locations
#     form_class = LocationForm
#     template_name = 'locations/locations_form.html'
#     success_url = reverse_lazy('locations-list')
#
# class LocationListView(ListView):
#     model = Locations
#     template_name = 'locations/location_list.html'
#     context_object_name = 'locations'
#
#     def get_queryset(self):
#         queryset = Locations.objects.all()
#         name_query = self.request.GET.get('name')
#         if name_query:
#             queryset = queryset.filter(name__icontains=name_query)
#         return queryset
#
# class LocationUpdateView(LoginRequiredMixin, UpdateView):
#     model = Locations
#     form_class = LocationForm
#     template_name = 'locations/locations_form.html'
#     success_url = reverse_lazy('locations-list')
#
# class LocationDeleteView(LoginRequiredMixin, DeleteView):
#     model = Locations
#     template_name = 'locations/locations_confirm_delete.html'
#     success_url = reverse_lazy('locations-list')
#
# def detail_location(request, location_id):
#     location = Locations.objects.get(id=location_id)
#     feedbacks = Feedback.objects.filter(location=location)
#     average_rating = calculate_average_rating(location_id)
#     return render(request, 'locations/location_detail.html', {'location': location, 'feedbacks': feedbacks, 'average_rating': average_rating})
#
#
# def filter_feedbacks_by_rate(request, pk):
#     feedbacks = Feedback.objects.filter(stars__gte=pk)  # Отримуємо всі відгуки
#
#     return render(request, 'locations/feedback_list.html', {'feedbacks': feedbacks})
#
#
# def filter_feedbacks_by_category(request):
#     if request.method == 'POST':
#         category = request.POST.get('category')
#         locations = Locations.objects.filter(category=category)
#         return render(request, 'locations/feedback_category_list.html', {'locations': locations})
#     else:
#         return render(request, 'locations/feedback_category_list.html', {'locations': []})
#
#
# def save_data(request):
#     locations = Locations.objects.all().values('name', 'average_rating', 'category')
#     locations_df = pd.DataFrame(locations)
#
#     # Експорт даних для Feedback
#     feedbacks = Feedback.objects.all().values('user__username', 'location__name', 'comments',
#                                                'comments_like', 'comments_dislike', 'stars')
#     feedbacks_df = pd.DataFrame(feedbacks)
#
#     # Створення CSV файлів у пам'яті
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="data_export.csv"'
#
#     # Запис у CSV файл
#     locations_df.to_csv('data1.csv', sep=';', index=False)
#     feedbacks_df.to_csv('data2.csv', sep=';', index=False)
#
#     return HttpResponse('All save correctly')
