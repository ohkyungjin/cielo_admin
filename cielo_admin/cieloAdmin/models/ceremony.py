from django.db import models
from django.core.validators import MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class Ceremony(models.Model):
    """예식 기본 정보"""
    STATUS_CHOICES = [
        ('active', '활성'),
        ('inactive', '비활성'),
        ('preparation', '준비중'),
    ]

    name = models.CharField(max_length=100, verbose_name='예식명')
    description = models.TextField(verbose_name='설명')
    short_description = models.CharField(max_length=200, verbose_name='짧은 설명')
    image = ProcessedImageField(
        upload_to='ceremonies/%Y/%m/',
        processors=[ResizeToFit(1200, 800)],
        format='JPEG',
        options={'quality': 85},
        verbose_name='예식 이미지'
    )
    
    # 가격 정보
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='기본 가격'
    )
    
    # 예식 상태 및 순서
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='preparation',
        verbose_name='상태'
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name='표시 순서')
    is_featured = models.BooleanField(default=False, verbose_name='추천 예식')
    
    # 통계
    reservation_count = models.PositiveIntegerField(default=0, verbose_name='예약 수')
    view_count = models.PositiveIntegerField(default=0, verbose_name='조회수')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '예식'
        verbose_name_plural = '예식 목록'
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def update_reservation_count(self):
        """예약 수 업데이트"""
        self.reservation_count = self.reservations.count()
        self.save()

class CeremonyOptionGroup(models.Model):
    """예식 옵션 그룹"""
    ceremony = models.ForeignKey(Ceremony, on_delete=models.CASCADE, related_name='option_groups', verbose_name='예식')
    name = models.CharField(max_length=100, verbose_name='옵션 그룹명')
    description = models.TextField(blank=True, null=True, verbose_name='설명')
    is_required = models.BooleanField(default=False, verbose_name='필수 선택')
    min_choices = models.PositiveIntegerField(default=0, verbose_name='최소 선택 수')
    max_choices = models.PositiveIntegerField(default=0, verbose_name='최대 선택 수')
    display_order = models.PositiveIntegerField(default=0, verbose_name='표시 순서')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '예식 옵션 그룹'
        verbose_name_plural = '예식 옵션 그룹 목록'
        ordering = ['display_order', 'created_at']

    def __str__(self):
        return f"{self.ceremony.name} - {self.name}"

class CeremonyOption(models.Model):
    """예식 옵션"""
    group = models.ForeignKey(CeremonyOptionGroup, on_delete=models.CASCADE, related_name='options', verbose_name='옵션 그룹')
    name = models.CharField(max_length=100, verbose_name='옵션명')
    description = models.TextField(blank=True, null=True, verbose_name='설명')
    image = ProcessedImageField(
        upload_to='ceremony_options/%Y/%m/',
        processors=[ResizeToFit(800, 600)],
        format='JPEG',
        options={'quality': 85},
        blank=True,
        null=True,
        verbose_name='옵션 이미지'
    )
    
    # 가격 정보
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='가격'
    )
    
    # 옵션 설정
    is_default = models.BooleanField(default=False, verbose_name='기본 선택')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    display_order = models.PositiveIntegerField(default=0, verbose_name='표시 순서')
    
    # 재고 관리
    stock = models.IntegerField(default=-1, verbose_name='재고 (-1: 무제한)')
    low_stock_threshold = models.PositiveIntegerField(default=5, verbose_name='부족 재고 기준')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '예식 옵션'
        verbose_name_plural = '예식 옵션 목록'
        ordering = ['display_order', 'created_at']
        unique_together = ['group', 'name']

    def __str__(self):
        return f"{self.group.name} - {self.name}"

    @property
    def is_low_stock(self):
        """재고 부족 여부"""
        if self.stock == -1:  # 무제한
            return False
        return self.stock <= self.low_stock_threshold

    @property
    def is_out_of_stock(self):
        """품절 여부"""
        if self.stock == -1:  # 무제한
            return False
        return self.stock <= 0
