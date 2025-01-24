from django.db import models
from django.conf import settings

class SystemLog(models.Model):
    """시스템 로그"""
    ACTION_CHOICES = [
        ('create', '생성'),
        ('update', '수정'),
        ('delete', '삭제'),
        ('login', '로그인'),
        ('logout', '로그아웃'),
        ('view', '조회'),
        ('export', '내보내기'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='system_logs',
        verbose_name='사용자'
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='작업')
    target_model = models.CharField(max_length=100, verbose_name='대상 모델')
    target_id = models.CharField(max_length=100, verbose_name='대상 ID')
    details = models.JSONField(default=dict, verbose_name='상세 정보')
    ip_address = models.GenericIPAddressField(verbose_name='IP 주소')
    user_agent = models.CharField(max_length=500, verbose_name='User Agent')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '시스템 로그'
        verbose_name_plural = '시스템 로그 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', 'action']),
            models.Index(fields=['target_model', 'target_id']),
        ]

    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.get_action_display()}"

class ErrorLog(models.Model):
    """에러 로그"""
    SEVERITY_CHOICES = [
        ('critical', '심각'),
        ('error', '에러'),
        ('warning', '경고'),
        ('info', '정보'),
    ]

    error_type = models.CharField(max_length=100, verbose_name='에러 유형')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, verbose_name='심각도')
    message = models.TextField(verbose_name='에러 메시지')
    stack_trace = models.TextField(verbose_name='스택 트레이스')
    request_data = models.JSONField(default=dict, verbose_name='요청 데이터')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='error_logs',
        verbose_name='사용자'
    )
    ip_address = models.GenericIPAddressField(null=True, verbose_name='IP 주소')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '에러 로그'
        verbose_name_plural = '에러 로그 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['error_type', 'severity']),
        ]

    def __str__(self):
        return f"{self.error_type} - {self.severity}"
