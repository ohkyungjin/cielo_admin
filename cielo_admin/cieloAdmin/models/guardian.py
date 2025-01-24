from django.db import models
from django.core.validators import RegexValidator

class Guardian(models.Model):
    name = models.CharField(max_length=100, verbose_name='보호자명')
    phone_regex = RegexValidator(
        regex=r'^\d{3}-\d{3,4}-\d{4}$',
        message="전화번호는 '010-1234-5678' 형식으로 입력해주세요."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=13,
        verbose_name='연락처'
    )
    email = models.EmailField(blank=True, null=True, verbose_name='이메일')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='주소')
    address_detail = models.CharField(max_length=100, blank=True, null=True, verbose_name='상세주소')
    postal_code = models.CharField(max_length=5, blank=True, null=True, verbose_name='우편번호')
    
    # 마케팅 수신 동의
    marketing_agree = models.BooleanField(default=False, verbose_name='마케팅 수신 동의')
    marketing_agree_date = models.DateTimeField(blank=True, null=True, verbose_name='마케팅 동의일')
    
    # 통계용 필드
    total_pets = models.PositiveIntegerField(default=0, verbose_name='총 반려동물 수')
    total_reservations = models.PositiveIntegerField(default=0, verbose_name='총 예약 수')
    last_visit_date = models.DateTimeField(blank=True, null=True, verbose_name='마지막 방문일')
    
    memo = models.TextField(blank=True, null=True, verbose_name='메모')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '보호자'
        verbose_name_plural = '보호자 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.phone})"

    def update_statistics(self):
        """보호자 통계 정보 업데이트"""
        self.total_pets = self.pets.count()
        self.total_reservations = self.reservations.count()
        if self.reservations.exists():
            self.last_visit_date = self.reservations.latest('created_at').created_at
        self.save()

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
        ('other', '기타'),
    ]

    SPECIES_CHOICES = [
        ('dog', '강아지'),
        ('cat', '고양이'),
        ('bird', '조류'),
        ('rabbit', '토끼'),
        ('hamster', '햄스터'),
        ('other', '기타'),
    ]

    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='pets', verbose_name='보호자')
    name = models.CharField(max_length=100, verbose_name='반려동물명')
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES, verbose_name='종류')
    breed = models.CharField(max_length=100, verbose_name='품종')
    age = models.IntegerField(verbose_name='나이')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='성별')
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='체중(kg)')
    
    # 사망 관련 정보
    death_date = models.DateTimeField(verbose_name='사망일시')
    death_cause = models.CharField(max_length=20, choices=DEATH_CAUSE_CHOICES, verbose_name='사망원인')
    death_cause_detail = models.TextField(blank=True, null=True, verbose_name='사망원인 상세')
    hospital_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='진료병원')
    hospital_contact = models.CharField(max_length=20, blank=True, null=True, verbose_name='병원연락처')
    
    # 추가 정보
    registration_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='동물등록번호')
    chip_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='칩번호')
    special_notes = models.TextField(blank=True, null=True, verbose_name='특이사항')
    
    # 방문 정보
    visit_path = models.CharField(max_length=100, blank=True, null=True, verbose_name='방문경로')
    reference_company = models.CharField(max_length=100, blank=True, null=True, verbose_name='경유업체')
    need_death_certificate = models.BooleanField(default=False, verbose_name='장례확인서 발급여부')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '반려동물'
        verbose_name_plural = '반려동물 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['guardian', 'name']),
            models.Index(fields=['death_date']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_species_display()} - {self.breed})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 보호자 통계 업데이트
        self.guardian.update_statistics()
