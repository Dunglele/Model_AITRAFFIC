from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TrafficCamera, TrafficHistory
from .serializers import TrafficCameraSerializer
import os

def index(request):
    """Trang Landing Page: Cho phep upload video demo va chon Case mo hinh"""
    return render(request, 'analytics/index.html')

def camera_list(request):
    query = request.GET.get('q', '')
    active_only = request.GET.get('active', 'false') == 'true'
    cameras_list = TrafficCamera.objects.all().order_by('title')
    
    if query:
        cameras_list = cameras_list.filter(title__icontains=query)
    if active_only:
        ten_minutes_ago = timezone.now() - timedelta(minutes=10)
        cameras_list = cameras_list.filter(last_updated__gte=ten_minutes_ago)
    
    paginator = Paginator(cameras_list, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'analytics/camera_list.html', {
        'page_obj': page_obj,
        'query': query,
        'active_only': active_only
    })

def camera_detail(request, pk):
    camera = get_object_or_404(TrafficCamera, pk=pk)
    # FIX: Lay dung 20 diem du lieu moi nhat de bieu do khong bi keo dai
    history_data = camera.history.all().order_by('-timestamp')[:20]
    return render(request, 'analytics/camera_detail.html', {
        'camera': camera,
        'history': reversed(history_data)
    })

def live_map(request):
    """Trang ban do nhiet hien thi trang thai giao thong toan thanh pho"""
    cameras = TrafficCamera.objects.all()
    return render(request, 'analytics/live_map.html', {'cameras': cameras})

class TrafficCameraViewSet(viewsets.ModelViewSet):
    queryset = TrafficCamera.objects.all().order_by('title')
    serializer_class = TrafficCameraSerializer

    @action(detail=False, methods=['post'])
    def upload_demo(self, request):
        """API nhan video demo va thuc thi traffic_platform.py"""
        video = request.FILES.get('video')
        mode = request.data.get('mode', 'fast')
        if not video:
            return Response({"error": "No video provided"}, status=400)
        
        # Logic: Luu tam va goi script subprocess (Giai doan tich hop sau)
        return Response({"message": f"Video dang duoc xu ly voi che do {mode}...", "status": "processing"})
