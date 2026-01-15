from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework import generics, response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .permissions import IsOwnerOrReadOnly


class FeedbacksListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        queryset = Feedback.objects.all()
        location_id = self.request.query_params.get("location_id")
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        return queryset

    def perform_create(self, serializer):
        # Check if user already provided feedback for this location
        location = serializer.validated_data.get('location')
        if Feedback.objects.filter(user=self.request.user, location=location).exists():
            raise ValidationError("You have already provided feedback for this location.")
        serializer.save(user=self.request.user)
        # Note: Signal handles average_rating update automatically


class FeedbackRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # Note: Signal handles average_rating update automatically
        return response.Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # Note: Signal handles average_rating update automatically
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
