import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aitraffic_web.settings')
django.setup()

from analytics.models import TrafficCamera

def init_coords():
    cameras = TrafficCamera.objects.all()
    count = 0
    for cam in cameras:
        # Toa do khu vuc trung tam TP.HCM
        cam.latitude = random.uniform(10.75, 10.80)
        cam.longitude = random.uniform(106.65, 106.70)
        cam.save()
        count += 1
    print(f"--- Da khoi tao toa do cho {count} camera ---")

if __name__ == '__main__':
    init_coords()
