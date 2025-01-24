from django.db import models
from django.core.exceptions import ValidationError
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Thumbnail
from .guardian import Pet, Guardian

def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB 제한
        raise ValidationError("최대 파일 크기는 10MB입니다.")

class MemorialSpace(models.Model):
    """추모공간 메인"""
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name='memorial_space', verbose_name='반려동물')
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='memorial_spaces', verbose_name='보호자')
    
    # 추모공간 설정
    title = models.CharField(max_length=200, verbose_name='추모공간 제목')
    cover_image = ProcessedImageField(upload_to='memorial/covers/%Y/%m/%d/',
                                    processors=[ResizeToFit(1920, 1080)],  # Full HD 크기로 리사이징
                                    format='JPEG',
                                    options={'quality': 85},
                                    validators=[validate_file_size],
                                    verbose_name='커버 이미지')
    
    background_music = models.FileField(
        upload_to='memorial/bgm/%Y/%m/%d/',
        validators=[validate_file_size],
        blank=True, 
        null=True,
        verbose_name='배경음악'
    )
    
    # 추모공간 상태
    is_public = models.BooleanField(default=True, verbose_name='공개 여부')
    view_count = models.PositiveIntegerField(default=0, verbose_name='조회수')
    
    # 기간 설정
    start_date = models.DateTimeField(verbose_name='시작일')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='종료일')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '추모공간'
        verbose_name_plural = '추모공간 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pet.name}의 추모공간 - {self.title}"

class MemorialPost(models.Model):
    """추모 게시글"""
    memorial_space = models.ForeignKey(MemorialSpace, on_delete=models.CASCADE, related_name='posts', verbose_name='추모공간')
    author = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='memorial_posts', verbose_name='작성자')
    
    # 게시글 내용
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    
    # 게시글 상태
    is_public = models.BooleanField(default=True, verbose_name='공개 여부')
    is_pinned = models.BooleanField(default=False, verbose_name='상단 고정')
    view_count = models.PositiveIntegerField(default=0, verbose_name='조회수')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '추모 게시글'
        verbose_name_plural = '추모 게시글 목록'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.author.name}"

class MemorialImage(models.Model):
    """추모 게시글 이미지"""
    post = models.ForeignKey(MemorialPost, on_delete=models.CASCADE, related_name='images', verbose_name='게시글')
    
    # 원본 이미지
    original_image = ProcessedImageField(
        upload_to='memorial/posts/%Y/%m/%d/original/',
        processors=[ResizeToFit(2000, 2000)],  # 최대 크기 제한
        format='JPEG',
        options={'quality': 85},
        validators=[validate_file_size],
        verbose_name='원본 이미지'
    )
    
    # 썸네일 이미지 (목록 표시용)
    thumbnail = ProcessedImageField(
        upload_to='memorial/posts/%Y/%m/%d/thumbnails/',
        processors=[Thumbnail(300, 300)],
        format='JPEG',
        options={'quality': 80},
        verbose_name='썸네일'
    )
    
    caption = models.CharField(max_length=200, blank=True, null=True, verbose_name='이미지 설명')
    order = models.PositiveIntegerField(default=0, verbose_name='정렬 순서')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '추모 이미지'
        verbose_name_plural = '추모 이미지 목록'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.post.title}의 이미지 {self.order}"

class MemorialComment(models.Model):
    """추모 게시글 댓글"""
    post = models.ForeignKey(MemorialPost, on_delete=models.CASCADE, related_name='comments', verbose_name='게시글')
    author = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='memorial_comments', verbose_name='작성자')
    content = models.TextField(verbose_name='내용')
    
    # 대댓글 구조
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='상위 댓글')
    
    is_public = models.BooleanField(default=True, verbose_name='공개 여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '추모 댓글'
        verbose_name_plural = '추모 댓글 목록'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.name}의 댓글"
