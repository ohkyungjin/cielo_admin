from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    """사용자 역할 정의"""
    name = models.CharField(max_length=50, unique=True, verbose_name='역할명')
    permissions = models.JSONField(default=dict, verbose_name='권한 목록')
    description = models.TextField(blank=True, null=True, verbose_name='설명')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '역할'
        verbose_name_plural = '역할 목록'
        ordering = ['name']

    def __str__(self):
        return self.name

class User(AbstractUser):
    """확장된 사용자 모델"""
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, related_name='users', verbose_name='역할')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='연락처')
    profile_image = models.ImageField(upload_to='profiles/%Y/%m/', blank=True, null=True, verbose_name='프로필 이미지')
    last_password_change = models.DateTimeField(blank=True, null=True, verbose_name='마지막 비밀번호 변경일')
    login_attempts = models.PositiveIntegerField(default=0, verbose_name='로그인 시도 횟수')
    is_locked = models.BooleanField(default=False, verbose_name='계정 잠금 여부')
    social_provider = models.CharField(max_length=20, blank=True, null=True, verbose_name='소셜 로그인 제공자')
    social_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='소셜 아이디')

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username
