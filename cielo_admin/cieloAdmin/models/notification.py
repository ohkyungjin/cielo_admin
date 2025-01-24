from django.db import models
from django.conf import settings

class NotificationTemplate(models.Model):
    """알림 템플릿"""
    TYPE_CHOICES = [
        ('reservation_confirm', '예약 확정'),
        ('status_change', '상태 변경'),
        ('reminder', '리마인더'),
        ('payment', '결제 알림'),
    ]
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, unique=True, verbose_name='템플릿 유형')
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    variables = models.JSONField(default=dict, verbose_name='템플릿 변수')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '알림 템플릿'
        verbose_name_plural = '알림 템플릿 목록'
        ordering = ['type']

    def __str__(self):
        return f"{self.get_type_display()} 템플릿"

class Notification(models.Model):
    """알림"""
    CHANNEL_CHOICES = [
        ('email', '이메일'),
        ('sms', 'SMS'),
        ('kakao', '카카오톡'),
    ]

    STATUS_CHOICES = [
        ('pending', '대기'),
        ('sent', '발송완료'),
        ('failed', '실패'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='수신자'
    )
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.PROTECT,
        related_name='notifications',
        verbose_name='알림 템플릿'
    )
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, verbose_name='발송 채널')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='상태')
    data = models.JSONField(default=dict, verbose_name='알림 데이터')
    is_read = models.BooleanField(default=False, verbose_name='읽음 여부')
    error_message = models.TextField(blank=True, null=True, verbose_name='에러 메시지')
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name='발송 시간')
    read_at = models.DateTimeField(blank=True, null=True, verbose_name='읽은 시간')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '알림'
        verbose_name_plural = '알림 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['status', 'channel']),
        ]

    def __str__(self):
        return f"{self.recipient.username}의 {self.get_channel_display()} 알림"
