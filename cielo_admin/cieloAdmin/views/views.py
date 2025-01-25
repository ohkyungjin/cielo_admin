from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'cieloAdmin/dashboard.html')

# 예약 관리
def reservation_list(request):
    return render(request, 'cieloAdmin/reservation/list.html')

def reservation_create(request):
    return render(request, 'cieloAdmin/reservation/create.html')

def reservation_create_pet(request):
    return render(request, 'cieloAdmin/reservation/create_pet.html')

def reservation_create_ceremony(request):
    return render(request, 'cieloAdmin/reservation/create_ceremony.html')

def reservation_create_confirm(request):
    return render(request, 'cieloAdmin/reservation/create_confirm.html')

# 서비스 관리
def service_list(request):
    return render(request, 'cieloAdmin/service/list.html')

def service_create(request):
    return render(request, 'cieloAdmin/service/create.html')

# 통계 분석
def statistics_index(request):
    return render(request, 'cieloAdmin/statistics/index.html')

# 추모 관리
def memorial_list(request):
    return render(request, 'cieloAdmin/memorial/list.html')

def memorial_create(request):
    return render(request, 'cieloAdmin/memorial/create.html')

# 시스템 설정
def settings_index(request):
    return render(request, 'cieloAdmin/settings/index.html')

# 캘린더
def calendar_index(request):
    return render(request, 'cieloAdmin/calendar/index.html')

# 사용자 관리
def user_list(request):
    return render(request, 'cieloAdmin/users/list.html')

def user_create(request):
    return render(request, 'cieloAdmin/users/create.html')

def user_edit(request, user_id):
    return render(request, 'cieloAdmin/users/edit.html')

# 알림 관리
def notification_list(request):
    return render(request, 'cieloAdmin/notifications/list.html')

def notification_settings(request):
    return render(request, 'cieloAdmin/notifications/settings.html')

# 로그 관리
def log_index(request):
    return render(request, 'cieloAdmin/logs/index.html')
