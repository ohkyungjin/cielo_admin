from django.apps import AppConfig


class CieloAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cieloAdmin"
    verbose_name = "반려동물 장례 서비스 관리자"

    def ready(self):
        """앱이 시작될 때 실행되는 코드"""
        try:
            import cieloAdmin.signals  # 시그널 등록
        except ImportError:
            pass
