from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import intcomma
from ..models.service import Service
from ..models import OptionGroup, Option

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
#@login_required
def service_list(request):
    services = Service.objects.all().order_by('-id')
    return render(request, 'cieloAdmin/service/list.html', {
        'services': services
    })

def service_create(request):
    """서비스 생성"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        base_price = request.POST.get('base_price')
        image = request.FILES.get('image')
        
        # 서비스 생성
        service = Service.objects.create(
            name=name,
            description=description,
            base_price=base_price,
            image=image,
        )
        
        # 선택된 옵션 그룹 저장
        for key, value in request.POST.items():
            if key.startswith('option_group_') and value:
                group_id = value
                group = OptionGroup.objects.get(id=group_id)
                service.option_groups.add(group)
        
        return redirect('cieloAdmin:service_list')
    
    # 모든 옵션 그룹 조회
    option_groups = OptionGroup.objects.prefetch_related('options').all().order_by('name')
    
    return render(request, 'cieloAdmin/service/create.html', {
        'option_groups': option_groups,
    })

def option_groups(request):
    """옵션 그룹 목록 페이지"""
    groups = OptionGroup.objects.all()
    return render(request, 'cieloAdmin/service/option_groups.html', {
        'groups': groups
    })

def option_group_create(request):
    """옵션 그룹 생성"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        group = OptionGroup.objects.create(
            name=name,
            description=description
        )
        
        return redirect('cieloAdmin:option_groups')
        
    return render(request, 'cieloAdmin/service/option_group_form.html')

def option_group_edit(request, group_id):
    """옵션 그룹 수정"""
    group = get_object_or_404(OptionGroup, id=group_id)
    
    if request.method == 'POST':
        group.name = request.POST.get('name')
        group.description = request.POST.get('description')
        group.save()
        return redirect('cieloAdmin:option_groups')
    
    return render(request, 'cieloAdmin/service/option_group_form.html', {
        'group': group
    })

def option_group_delete(request, group_id):
    """옵션 그룹 삭제"""
    group = get_object_or_404(OptionGroup, id=group_id)
    group.delete()
    return redirect('cieloAdmin:option_groups')

def option_create(request, group_id):
    """옵션 추가"""
    group = get_object_or_404(OptionGroup, id=group_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        
        Option.objects.create(
            group=group,
            name=name,
            price=price
        )
        
        return redirect('cieloAdmin:option_group_edit', group_id=group.id)
        
    return render(request, 'cieloAdmin/service/option_form.html', {
        'group': group
    })

def option_edit(request, option_id):
    """옵션 수정"""
    option = get_object_or_404(Option, id=option_id)
    
    if request.method == 'POST':
        option.name = request.POST.get('name')
        option.price = request.POST.get('price')
        option.save()
        
        return redirect('cieloAdmin:option_group_edit', group_id=option.group.id)
        
    return render(request, 'cieloAdmin/service/option_form.html', {
        'option': option,
        'group': option.group
    })

def option_delete(request, option_id):
    """옵션 삭제"""
    option = get_object_or_404(Option, id=option_id)
    group_id = option.group.id
    option.delete()
    return redirect('cieloAdmin:option_group_edit', group_id=group_id)

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
#@login_required
def calendar(request):
    services = Service.objects.all()
    return render(request, 'cieloAdmin/calendar/index.html', {'services': services})

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
