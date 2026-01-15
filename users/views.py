from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


class RegisterAPIView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Registration failed", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProtectedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"message": "This is a protected view"}, status=status.HTTP_200_OK
        )


class LoginView(APIView):
    def get(self, request):
        return Response(
            {"message": "GET method is not allowed. Use POST to login."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return Response(
                {
                    "message": "Logged in successfully",
                    "user_id": user.id,
                    "username": user.username,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials", "details": form.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutView(APIView):
    def get(self, request):
        return Response(
            {"message": "GET method is not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def post(self, request):
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


def home(request):
    return HttpResponse("Hello, World!")


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.subscription = not user.subscription
        user.save()
        return Response(
            {"message": "Subscription status updated"}, status=status.HTTP_200_OK
        )
