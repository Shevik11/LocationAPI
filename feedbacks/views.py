from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework import generics, response, status

# Create your views here.


class FeedbacksListCreateAPIView(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        queryset = Feedback.objects.all()
        name_query = self.request.query_params.get("name")
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)
        return queryset


class LocationsRetrieveUpdateDestroyAPIView(
    LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Feedback.objects.filter(location=instance).delete()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


# class FeedbackCreateView(LoginRequiredMixin, CreateView):
#     model = Feedback
#     form_class = FeedbackForm
#     template_name = 'locations/feedback_form.html'
#     success_url = reverse_lazy('locations-list')
#
#     def form_valid(self, form):
#         user = User.objects.get(pk=self.request.user.pk)  # Примусово отримуємо CustomUser
#         form.instance.user = user
#         return super().form_valid(form)
#
# class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
#     model = Feedback
#     form_class = FeedbackForm
#     template_name = 'locations/feedback_form.html'
#     success_url = reverse_lazy('locations-list')
#
#     def get_queryset(self):
#         return Feedback.objects.filter(user=self.request.user)
#
#     def form_valid(self, form):
#         form.instance.user = User.objects.get(pk=self.request.user.pk)  # Примусово отримуємо CustomUser
#         return super().form_valid(form)
#
# class FeedbackDeleteView(LoginRequiredMixin, DeleteView):
#     model = Feedback
#     template_name = 'locations/feedback_confirm_delete.html'
#     success_url = reverse_lazy('locations-list')
#
#     def get_queryset(self):
#         return Feedback.objects.filter(user=self.request.user)
