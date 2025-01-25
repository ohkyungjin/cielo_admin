from django.db import models
from django.utils import timezone

class Service(models.Model):
    """예식 서비스"""
    name = models.CharField('예식명', max_length=100, default='')
    description = models.TextField('설명', default='')
    base_price = models.IntegerField('기본 가격', default=0)
    image = models.ImageField('대표 이미지', upload_to='services/', null=True, blank=True)
    option_groups = models.ManyToManyField('OptionGroup', verbose_name='옵션 그룹', blank=True)
    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '예식'
        verbose_name_plural = '예식'
        ordering = ['-created_at']

class OptionGroup(models.Model):
    """옵션 그룹"""
    name = models.CharField('그룹명', max_length=100, default='')
    description = models.TextField('설명', blank=True, default='')
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

class Option(models.Model):
    """옵션"""
    group = models.ForeignKey(OptionGroup, verbose_name='옵션 그룹',
                            related_name='options',
                            on_delete=models.CASCADE)
    name = models.CharField('옵션명', max_length=100, default='')
    price = models.IntegerField('가격', default=0)
    created_at = models.DateTimeField('등록일', default=timezone.now)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        verbose_name = '옵션'
        verbose_name_plural = '옵션'
        ordering = ['group', '-created_at']

    def __str__(self):
        return f'{self.group.name} - {self.name}'
