from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from .guardian import Guardian, Pet
from .ceremony import Ceremony, CeremonyOption

class Reservation(models.Model):
    """예약 정보"""
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('confirmed', '확정'),
        ('in_progress', '진행중'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', '결제대기'),
        ('paid', '결제완료'),
        ('partial', '부분결제'),
        ('refunded', '환불'),
        ('cancelled', '취소'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', '카드'),
        ('cash', '현금'),
        ('transfer', '계좌이체'),
        ('other', '기타'),
    ]

    # 기본 정보
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.PROTECT,
        related_name='reservations',
        verbose_name='보호자'
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.PROTECT,
        related_name='reservations',
        verbose_name='반려동물'
    )
    ceremony = models.ForeignKey(
        Ceremony,
        on_delete=models.PROTECT,
        related_name='reservations',
        verbose_name='예식'
    )
    assigned_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_reservations',
        verbose_name='담당 직원'
    )
    
    # 예약 상태
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='예약상태'
    )
    
    # 예약 정보
    reservation_number = models.CharField(max_length=20, unique=True, verbose_name='예약번호')
    reservation_date = models.DateTimeField(verbose_name='예약일시')
    expected_duration = models.DurationField(verbose_name='예상 소요시간')
    special_requests = models.TextField(blank=True, null=True, verbose_name='특별 요청사항')
    
    # 비용 정보
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='기본 가격'
    )
    additional_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='추가 가격'
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='할인 금액'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='총 가격'
    )
    
    # 결제 정보
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='결제상태'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True,
        verbose_name='결제수단'
    )
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='결제금액'
    )
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name='결제일시')
    
    # 서명 정보
    signature = models.TextField(verbose_name='서명')  # Base64 encoded signature
    signature_date = models.DateTimeField(auto_now_add=True, verbose_name='서명일시')
    
    # 기타 정보
    memo = models.TextField(blank=True, null=True, verbose_name='관리자 메모')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '예약'
        verbose_name_plural = '예약 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reservation_number']),
            models.Index(fields=['reservation_date']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"{self.reservation_number} - {self.pet.name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # 총 가격 계산
        if not self.total_price:
            self.total_price = self.base_price + self.additional_price - self.discount_amount
        
        # 저장
        super().save(*args, **kwargs)
        
        # 예식 예약 수 업데이트
        self.ceremony.update_reservation_count()
        
        # 보호자 통계 업데이트
        self.guardian.update_statistics()

class ReservationCeremonyOption(models.Model):
    """예약에 선택된 예식 옵션"""
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='selected_options',
        verbose_name='예약'
    )
    option = models.ForeignKey(
        CeremonyOption,
        on_delete=models.PROTECT,
        related_name='reservation_selections',
        verbose_name='선택된 옵션'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='수량')
    price_at_time = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='선택 당시 가격'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '예약 예식 옵션'
        verbose_name_plural = '예약 예식 옵션 목록'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.reservation.reservation_number} - {self.option.name}"

    def save(self, *args, **kwargs):
        # 처음 생성시 현재 옵션 가격 저장
        if not self.price_at_time:
            self.price_at_time = self.option.price
        super().save(*args, **kwargs)
