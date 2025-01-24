from django.db import models
from django.core.validators import MinValueValidator
from .ceremony import Ceremony
from .payment import Payment

class DailyRevenue(models.Model):
    """일별 매출 통계"""
    date = models.DateField(unique=True, verbose_name='날짜')
    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='총 매출액'
    )
    reservation_count = models.PositiveIntegerField(default=0, verbose_name='예약 수')
    cancellation_count = models.PositiveIntegerField(default=0, verbose_name='취소 수')
    average_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='평균 매출액'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '일별 매출'
        verbose_name_plural = '일별 매출 목록'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.date} 매출"

class ServiceStatistics(models.Model):
    """서비스별 통계"""
    PERIOD_CHOICES = [
        ('daily', '일별'),
        ('weekly', '주별'),
        ('monthly', '월별'),
    ]

    ceremony = models.ForeignKey(
        Ceremony,
        on_delete=models.CASCADE,
        related_name='statistics',
        verbose_name='예식'
    )
    period_type = models.CharField(max_length=20, choices=PERIOD_CHOICES, verbose_name='기간 유형')
    period_start = models.DateTimeField(verbose_name='기간 시작')
    period_end = models.DateTimeField(verbose_name='기간 종료')
    reservation_count = models.PositiveIntegerField(default=0, verbose_name='예약 수')
    cancellation_count = models.PositiveIntegerField(default=0, verbose_name='취소 수')
    total_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='총 매출액'
    )
    average_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='평균 매출액'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '서비스 통계'
        verbose_name_plural = '서비스 통계 목록'
        ordering = ['-period_start']
        indexes = [
            models.Index(fields=['ceremony', 'period_type', '-period_start']),
        ]
        unique_together = ['ceremony', 'period_type', 'period_start']

    def __str__(self):
        return f"{self.ceremony.name} {self.get_period_type_display()} 통계"

class PaymentMethodStatistics(models.Model):
    """결제수단별 통계"""
    date = models.DateField(verbose_name='날짜')
    payment_method = models.CharField(
        max_length=20,
        choices=Payment.METHOD_CHOICES,
        verbose_name='결제수단'
    )
    transaction_count = models.PositiveIntegerField(default=0, verbose_name='거래 수')
    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='총 금액'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '결제수단별 통계'
        verbose_name_plural = '결제수단별 통계 목록'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date', 'payment_method']),
        ]
        unique_together = ['date', 'payment_method']

    def __str__(self):
        return f"{self.date} {self.get_payment_method_display()} 통계"
