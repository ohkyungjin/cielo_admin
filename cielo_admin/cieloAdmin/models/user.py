from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', '관리자'),
        ('manager', '매니저'),
        ('staff', '직원'),
    ]

    phone = models.CharField(max_length=20, blank=True, verbose_name='연락처')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff', verbose_name='역할')
    profile_image = models.ImageField(upload_to='profiles/%Y/%m/%d/', blank=True, null=True, verbose_name='프로필 이미지')
    last_login_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name='마지막 로그인 IP')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"
