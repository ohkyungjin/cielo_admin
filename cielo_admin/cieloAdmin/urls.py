from django.urls import path
from .views.views import (
    index, 
    reservation_list, reservation_create, reservation_create_pet,
    reservation_create_ceremony, reservation_create_confirm,
    service_list, service_create,
    statistics_index,
    memorial_list, memorial_create,
    settings_index,
    calendar_index,
    user_list, user_create, user_edit,
    notification_list, notification_settings,
    log_index
)
from .views.auth import login

app_name = 'cieloAdmin'

urlpatterns = [
    # 대시보드
    path('', index, name='index'),
    
    # 인증
    path('login/', login, name='login'),
    
    # 예약 관리
    path('reservation/', reservation_list, name='reservation_list'),
    path('reservation/create/', reservation_create, name='reservation_create'),
    path('reservation/create/pet/', reservation_create_pet, name='reservation_create_pet'),
    path('reservation/create/ceremony/', reservation_create_ceremony, name='reservation_create_ceremony'),
    path('reservation/create/confirm/', reservation_create_confirm, name='reservation_create_confirm'),
    
    # 서비스 관리
    path('service/', service_list, name='service_list'),
    path('service/create/', service_create, name='service_create'),
    
    # 통계 분석
    path('statistics/', statistics_index, name='statistics_index'),
    
    # 추모 관리
    path('memorial/', memorial_list, name='memorial_list'),
    path('memorial/create/', memorial_create, name='memorial_create'),
    
    # 시스템 설정
    path('settings/', settings_index, name='settings_index'),

    # 캘린더
    path('calendar/', calendar_index, name='calendar_index'),
    
    # 사용자 관리
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:user_id>/edit/', user_edit, name='user_edit'),
    
    # 알림 관리
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/settings/', notification_settings, name='notification_settings'),
    
    # 로그 관리
    path('logs/', log_index, name='log_index'),
]