from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('accounts', views.CustomUserCreateViewSet)


app_name = 'users'
urlpatterns = [
    # path('account/', views.CustomUserCreateApiView.as_view(), name='register')
    path('', include(router.urls)),
]
