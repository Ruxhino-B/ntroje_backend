from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UpdateProfileSerializer,
    UserMeSerializer,
)


class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Body: { email, password }
    Response: { access, refresh, user: { id, email, username, full_name, role, avatar } }
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Body: { email, username, first_name, last_name, phone, password, password_confirm }
    Response: 201 + user data
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserMeSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Body: { refresh }
    Blacklists the refresh token so it can no longer be used.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/auth/me/  → returns current user profile
    PATCH /api/auth/me/ → updates first_name, last_name, username, phone, avatar
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UpdateProfileSerializer
        return UserMeSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ChangePasswordView(APIView):
    """
    POST /api/auth/change-password/
    Body: { old_password, new_password, new_password_confirm }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)
