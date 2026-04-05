from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TrafficCamera, TrafficHistory
from .serializers import TrafficCameraSerializer
from .ai_utils import analyze_image
import os

def camera_list(request):
    query = request.GET.get('q', '')
    active_only = request.GET.get('active', 'false') == 'true'
    
    cameras_list = TrafficCamera.objects.all().order_by('title')
    
    # Loc theo ten
    if query:
        cameras_list = cameras_list.filter(title__icontains=query)
    
    # Loc camera dang hoat dong (co cap nhat trong 10 phut qua)
    if active_only:
        ten_minutes_ago = timezone.now() - timedelta(minutes=10)
        cameras_list = cameras_list.filter(last_updated__gte=ten_minutes_ago)
    
    paginator = Paginator(cameras_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'analytics/camera_list.html', {
        'page_obj': page_obj,
        'query': query,
        'active_only': active_only
    })

def camera_detail(request, pk):
    camera = get_object_or_404(TrafficCamera, pk=pk)
    # Chi lay 20 ban ghi lich su moi nhat de ve bieu do (fix loi keo dai)
    history = camera.history.all().order_by('-timestamp')[:20]
    return render(request, 'analytics/camera_detail.html', {
        'camera': camera,
        'history': reversed(history) # Dao nguoc de ve tu trai sang phai
    })

class TrafficCameraViewSet(viewsets.ModelViewSet):
    queryset = TrafficCamera.objects.all().order_by('title')
    serializer_class = TrafficCameraSerializer

    @action(detail=True, methods=['post'])
    def process_frame(self, request, pk=None):
        camera = self.get_object()
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
        camera.last_image = image_file
        camera.save()
        results = analyze_image(camera.last_image.path)
        camera.current_density = results['density']
        camera.current_vehicle_count = results['vehicle_count']
        camera.current_traffic_level = results['traffic_level']
        camera.save()
        TrafficHistory.objects.create(camera=camera, density_pce=results['density'], vehicle_count=results['vehicle_count'], traffic_level=results['traffic_level'])
        return Response(results)
