from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .reservation import Reservation

class Payment(models.Model):
    """결제 정보"""
    METHOD_CHOICES = [
        ('card', '신용카드'),
        ('transfer', '계좌이체'),
        ('vbank', '가상계좌'),
        ('cash', '현금'),
    ]

    STATUS_CHOICES = [
        ('pending', '결제대기'),
        ('paid', '결제완료'),
        ('cancelled', '취소'),
        ('refunded', '환불'),
        ('failed', '실패'),
    ]

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name='예약'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='결제금액'
    )
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, verbose_name='결제수단')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='상태')
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name='거래번호')
    payment_key = models.CharField(max_length=100, blank=True, null=True, verbose_name='결제 키')
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name='결제완료시간')
    
    # 카드 결제 정보
    card_company = models.CharField(max_length=50, blank=True, null=True, verbose_name='카드사')
    card_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='카드번호')
    installment_months = models.PositiveIntegerField(default=0, verbose_name='할부개월')
    
    # 계좌이체/가상계좌 정보
    bank_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='은행명')
    account_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='계좌번호')
    
    # 환불 정보
    refund_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='환불금액'
    )
    refund_reason = models.TextField(blank=True, null=True, verbose_name='환불사유')
    refunded_at = models.DateTimeField(blank=True, null=True, verbose_name='환불시간')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '결제'
        verbose_name_plural = '결제 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reservation', '-created_at']),
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status', 'method']),
        ]

    def __str__(self):
        return f"{self.reservation.id}의 결제 ({self.get_status_display()})"

class Discount(models.Model):
    """할인 정책"""
    TYPE_CHOICES = [
        ('percentage', '비율'),
        ('fixed', '고정금액'),
    ]

    name = models.CharField(max_length=100, verbose_name='할인명')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='할인유형')
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='할인값'
    )
    max_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        verbose_name='최대할인금액'
    )
    start_date = models.DateTimeField(verbose_name='시작일시')
    end_date = models.DateTimeField(verbose_name='종료일시')
    max_use_count = models.PositiveIntegerField(default=0, verbose_name='최대사용횟수')
    used_count = models.PositiveIntegerField(default=0, verbose_name='사용횟수')
    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='최소주문금액'
    )
    is_active = models.BooleanField(default=True, verbose_name='활성화여부')
    description = models.TextField(blank=True, null=True, verbose_name='설명')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '할인'
        verbose_name_plural = '할인 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name

class ReservationDiscount(models.Model):
    """예약에 적용된 할인"""
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='applied_discounts',
        verbose_name='예약'
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.PROTECT,
        related_name='reservation_discounts',
        verbose_name='할인'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='할인금액'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '적용된 할인'
        verbose_name_plural = '적용된 할인 목록'
        ordering = ['-created_at']
        unique_together = ['reservation', 'discount']

    def __str__(self):
        return f"{self.reservation.id}의 {self.discount.name} 할인"
