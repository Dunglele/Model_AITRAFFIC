import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from analytics.models import TrafficCamera, TrafficHistory
from analytics.ai_utils import analyze_image
from datetime import datetime
from time import sleep

class Command(BaseCommand):
    help = 'Cao anh tu website giao thong voi Headers/Cookies chuan va cap nhat AI'

    def handle(self, *args, **options):
        # Bộ Headers sao chép từ crawl_datatraffic.py
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Accept": "image/avif,image/webp,*/*",
            "Referer": "https://giaothong.hochiminhcity.gov.vn/",
            "Origin": "https://giaothong.hochiminhcity.gov.vn",
        }

        # Bộ Cookies sao chép từ crawl_datatraffic.py
        cookies = {
            "ASP.NET_SessionId": "t2oslxxsqllan4lgzhah3cgt",
            ".VDMS": "C50F85C6C71667BE6ED050D74003980406811A8F6C3BE32B157BABF3CD92E74B0BA3E01A4B490B8BA16EAF15828702B1FB68957AD67317B9D42579BB90FCC150AF18CA519E195678537CA47740D9831A7E454628FC6A4097185A66629BB114F7EE9611E85CE9747C30D5968598EFBF67382F9DD1",
            "_frontend": "!9YOHO1qc4zwwKz24P1VY/lC/bQptjssYZ3m9UbDnTWnCQqqoOil+geXpFacMNljkY7bQh63nOwwyIko=",
            "CurrentLanguage": "vi",
        }
        
        cameras = TrafficCamera.objects.exclude(camera_id__isnull=True)
        
        while True:
            self.stdout.write(self.style.SUCCESS(f"--- Bat dau chu ky cap nhat luc {datetime.now()} ---"))
            
            for camera in cameras:
                url = f"https://giaothong.hochiminhcity.gov.vn:8007/Render/CameraHandler.ashx?id={camera.camera_id}&bg=black&w=640&h=480"
                
                try:
                    # Gửi request với cả Headers và Cookies để tránh lỗi 403
                    resp = requests.get(url, headers=headers, cookies=cookies, timeout=15)
                    
                    if resp.status_code == 200:
                        # 1. Luu anh truc tiep vao ban ghi Database
                        file_name = f"{camera.camera_id}.jpg"
                        camera.last_image.save(file_name, ContentFile(resp.content), save=False)
                        
                        # 2. Chay AI phan tich (Dung duong dan file da luu)
                        results = analyze_image(camera.last_image.path)
                        
                        # 3. Cap nhat Database tong the
                        camera.current_density = results['density']
                        camera.current_vehicle_count = results['vehicle_count']
                        camera.current_traffic_level = results['traffic_level']
                        camera.save() # Save thuc su tai day
                        
                        # 4. Luu lich su
                        TrafficHistory.objects.create(
                            camera=camera,
                            density_pce=results['density'],
                            vehicle_count=results['vehicle_count'],
                            traffic_level=results['traffic_level']
                        )
                        self.stdout.write(self.style.SUCCESS(f" OK -> {camera.title}: {results['density']}%"))
                    else:
                        self.stdout.write(self.style.WARNING(f" Loi {resp.status_code} tai {camera.title}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f" Loi tai {camera.title}: {str(e)}"))
            
            self.stdout.write(self.style.SUCCESS("--- Hoan tat chu ky. Cho 60 giay... ---"))
            sleep(60)
