from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import TrafficCamera, TrafficHistory, DemoResult
from .serializers import TrafficCameraSerializer
from rest_framework import viewsets
import os
import json
import subprocess
import pandas as pd
import time

def index(request):
    return render(request, 'analytics/index.html')

def camera_list(request):
    query = request.GET.get('q', '')
    active_only = request.GET.get('active', 'false') == 'true'
    cameras_list = TrafficCamera.objects.all().order_by('title')
    if query:
        cameras_list = cameras_list.filter(title__icontains=query)
    from datetime import timedelta
    if active_only:
        ten_minutes_ago = timezone.now() - timedelta(minutes=10)
        cameras_list = cameras_list.filter(last_updated__gte=ten_minutes_ago)
    paginator = Paginator(cameras_list, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'analytics/camera_list.html', {'page_obj': page_obj, 'query': query, 'active_only': active_only})

def camera_detail(request, pk):
    camera = get_object_or_404(TrafficCamera, pk=pk)
    history = camera.history.all().order_by('-timestamp')[:20]
    return render(request, 'analytics/camera_detail.html', {'camera': camera, 'history': reversed(history)})

def live_map(request):
    cameras = TrafficCamera.objects.all()
    hotspots = TrafficCamera.objects.all().order_by('-current_density')[:5]
    return render(request, 'analytics/live_map.html', {'cameras': cameras, 'hotspots': hotspots})

def demo_upload(request):
    if request.method == 'POST':
        video = request.FILES.get('video')
        mode = request.POST.get('mode', 'fast')
        if video:
            try:
                result = DemoResult.objects.create(video_file=video, mode=mode)
                input_path = result.video_file.path
                
                # CHUYEN SANG .WEBM DE TUONG THICH WEB
                output_filename = f"processed_{result.id}.webm"
                report_filename = f"report_{result.id}.csv"
                progress_filename = f"progress_{result.id}.txt"
                
                output_dir = os.path.join(os.getcwd(), 'media', 'demo_results')
                if not os.path.exists(output_dir): os.makedirs(output_dir)
                
                output_path = os.path.join(output_dir, output_filename)
                report_path = os.path.join(output_dir, report_filename)
                progress_path = os.path.join(output_dir, progress_filename)
                
                with open(progress_path, 'w') as f: f.write("0")
                
                python_exe = os.path.join(os.getcwd(), 'env', 'bin', 'python3')
                cmd = [
                    python_exe, "traffic_platform.py",
                    "--input", input_path,
                    "--output", output_path,
                    "--mode", mode,
                    "--report", report_path,
                    "--progress", progress_path
                ]
                
                process = subprocess.run(cmd, capture_output=True, text=True)
                if process.returncode != 0:
                    return JsonResponse({'status': 'error', 'message': f"AI Error: {process.stderr}"}, status=500)
                
                if os.path.exists(report_path):
                    df = pd.read_csv(report_path)
                    result.analytics_json = df.to_json(orient='records')
                    result.total_vehicles = int(df['total_vehicles'].max()) if 'total_vehicles' in df.columns else 0
                    result.peak_density = float(df['density_pce'].max()) if 'density_pce' in df.columns else 0
                
                result.processed_video = f"demo_results/{output_filename}"
                result.save()
                return JsonResponse({'status': 'success', 'id': result.id})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def get_progress(request, pk):
    progress_path = os.path.join(os.getcwd(), 'media', 'demo_results', f'progress_{pk}.txt')
    if os.path.exists(progress_path):
        with open(progress_path, 'r') as f:
            percent = f.read().strip()
            return JsonResponse({'progress': percent})
    return JsonResponse({'progress': '0'})

def demo_result(request, pk):
    result = get_object_or_404(DemoResult, pk=pk)
    return render(request, 'analytics/demo_result.html', {
        'result': result,
        'analytics': json.loads(result.analytics_json) if result.analytics_json else []
    })

class TrafficCameraViewSet(viewsets.ModelViewSet):
    queryset = TrafficCamera.objects.all().order_by('title')
    serializer_class = TrafficCameraSerializer
