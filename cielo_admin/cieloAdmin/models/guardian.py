from django.db import models

class Guardian(models.Model):
    name = models.CharField(max_length=100, verbose_name='보호자명')
    phone = models.CharField(max_length=20, verbose_name='연락처')
    email = models.EmailField(blank=True, null=True, verbose_name='이메일')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='주소')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '보호자'
        verbose_name_plural = '보호자 목록'

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Pet(models.Model):
    GENDER_CHOICES = [
        ('M', '수컷'),
        ('F', '암컷'),
    ]

    DEATH_CAUSE_CHOICES = [
        ('natural', '자연사'),
        ('disease', '병사'),
        ('accident', '사고사'),
        ('euthanasia', '안락사'),
    ]

    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='pets', verbose_name='보호자')
    name = models.CharField(max_length=100, verbose_name='반려동물명')
    species = models.CharField(max_length=50, verbose_name='품종')
    age = models.IntegerField(verbose_name='나이')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='성별')
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='체중(kg)')
    death_date = models.DateTimeField(verbose_name='사망일시')
    death_cause = models.CharField(max_length=20, choices=DEATH_CAUSE_CHOICES, verbose_name='사망원인')
    death_cause_detail = models.TextField(blank=True, null=True, verbose_name='사망원인 상세')
    
    # 추가 정보
    visit_path = models.CharField(max_length=100, blank=True, null=True, verbose_name='방문경로')
    reference_company = models.CharField(max_length=100, blank=True, null=True, verbose_name='경유업체')
    need_death_certificate = models.BooleanField(default=False, verbose_name='장례확인서 발급여부')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '반려동물'
        verbose_name_plural = '반려동물 목록'

    def __str__(self):
        return f"{self.name} ({self.species}) - {self.guardian.name}"
