from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrafficCameraViewSet, camera_list, camera_detail

router = DefaultRouter()
router.register(r'cameras', TrafficCameraViewSet)

urlpatterns = [
    path('', camera_list, name='camera_list'),
    path('camera/<int:pk>/', camera_detail, name='camera_detail'),
    path('api/', include(router.urls)),
]
