from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrafficCameraViewSet, camera_list, camera_detail, index, live_map

router = DefaultRouter()
router.register(r'cameras', TrafficCameraViewSet)

urlpatterns = [
    path('', index, name='index'), 
    path('list/', camera_list, name='camera_list'), 
    path('map/', live_map, name='live_map'), # URL ban do moi
    path('camera/<int:pk>/', camera_detail, name='camera_detail'),
    path('api/', include(router.urls)),
]
