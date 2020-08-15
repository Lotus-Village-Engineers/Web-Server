from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

# router = DefaultRouter()
# router.register('users', views.CustomUserCreateViewSet)


app_name = 'users'
urlpatterns = [
    path('users/register', views.CustomUserCreateApiView.as_view(), name='register'),
    path('users/me', views.CustomUserManageApiView.as_view(), name='manage'),
    path('users/token', TokenObtainPairView.as_view(), name='login'),
    path('users/refresh', TokenRefreshView.as_view(), name='token-refresh'),
]