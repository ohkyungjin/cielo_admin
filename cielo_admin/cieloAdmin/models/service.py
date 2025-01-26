from django.db import models
from django.utils import timezone

class Service(models.Model):
    """예식 서비스"""
    name = models.CharField('예식명', max_length=100, default='')
    description = models.TextField('설명', default='')
    base_price = models.IntegerField('기본 가격', default=0)
    image = models.ImageField('대표 이미지', upload_to='services/', null=True, blank=True)
    option_groups = models.ManyToManyField('OptionGroup', verbose_name='옵션 그룹', blank=True)
    options = models.ManyToManyField('Option', verbose_name='선택된 옵션', blank=True)
    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    status = models.CharField('상태', max_length=20, choices=[
        ('active', '활성'),
        ('inactive', '비활성')
    ], default='active')
    is_default = models.BooleanField('기본 서비스 여부', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '예식'
        verbose_name_plural = '예식'
        ordering = ['-created_at']

    @classmethod
    def get_default_service(cls):
        """기본 서비스 조회"""
        return cls.objects.filter(is_default=True, status='active').first()

    def clone_options_from(self, source_service):
        """다른 서비스의 옵션을 복사"""
        if source_service:
            self.option_groups.set(source_service.option_groups.all())
            self.options.set(source_service.options.all())

class OptionGroup(models.Model):
    """옵션 그룹"""
    name = models.CharField('그룹명', max_length=100, default='')
    description = models.TextField('설명', blank=True, default='')
    required = models.BooleanField('필수 여부', default=False)
    multiple = models.BooleanField('다중 선택 가능', default=False)
    is_default = models.BooleanField('기본 그룹 여부', default=False)
    created_at = models.DateTimeField('등록일', default=timezone.now)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '옵션 그룹'
        verbose_name_plural = '옵션 그룹'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def options_count(self):
        """그룹에 포함된 옵션 개수"""
        return self.options.count()

    @classmethod
    def get_default_groups(cls):
        """기본 옵션 그룹 조회"""
        return cls.objects.filter(is_default=True)

class Option(models.Model):
    """옵션"""
    group = models.ForeignKey(OptionGroup, verbose_name='옵션 그룹',
                            related_name='options',
                            on_delete=models.CASCADE)
    name = models.CharField('옵션명', max_length=100, default='')
    price = models.IntegerField('가격', default=0)
    is_default = models.BooleanField('기본 옵션 여부', default=False)
    created_at = models.DateTimeField('등록일', default=timezone.now)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '옵션'
        verbose_name_plural = '옵션'
        ordering = ['group', '-created_at']

    def __str__(self):
        return f'{self.group.name} - {self.name}'

    @classmethod
    def get_default_options(cls):
        """기본 옵션 조회"""
        return cls.objects.filter(is_default=True)
