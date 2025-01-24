from django.db import models
from .guardian import Guardian, Pet

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='서비스명')
    description = models.TextField(verbose_name='설명')
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='기본 가격')
    status = models.CharField(max_length=20, choices=[
        ('active', '활성'),
        ('inactive', '비활성'),
    ], verbose_name='상태')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '서비스'
        verbose_name_plural = '서비스 목록'

    def __str__(self):
        return self.name

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('confirmed', '확정'),
        ('in_progress', '진행중'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    ]

    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='reservations', verbose_name='보호자')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reservations', verbose_name='반려동물')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reservations', verbose_name='서비스')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='상태')
    
    # 예약 정보
    reservation_date = models.DateTimeField(verbose_name='예약일시')
    special_requests = models.TextField(blank=True, null=True, verbose_name='특별 요청사항')
    
    # 비용 정보
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='기본 가격')
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='추가 가격')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='총 가격')
    
    # 서명 정보
    signature = models.TextField(verbose_name='서명')  # Base64 encoded signature
    signature_date = models.DateTimeField(auto_now_add=True, verbose_name='서명일시')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '예약'
        verbose_name_plural = '예약 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pet.name} - {self.service.name} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.base_price + self.additional_price
        super().save(*args, **kwargs)
