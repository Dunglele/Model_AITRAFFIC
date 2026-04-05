from django.db import models

class TrafficCamera(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tên Camera")
    camera_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="ID Camera (Hex)")
    image_source_url = models.URLField(null=True, blank=True, verbose_name="URL Ảnh trực tiếp")
    last_image = models.ImageField(upload_to='live_snapshots/', null=True, blank=True)
    
    # Thống kê hiện tại
    current_density = models.FloatField(default=0.0)
    current_vehicle_count = models.IntegerField(default=0)
    current_traffic_level = models.CharField(max_length=50, default="Thông thoáng")
    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TrafficHistory(models.Model):
    camera = models.ForeignKey(TrafficCamera, on_delete=models.CASCADE, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True)
    density_pce = models.FloatField()
    vehicle_count = models.IntegerField()
    traffic_level = models.CharField(max_length=50)

    class Meta:
        ordering = ['-timestamp']
