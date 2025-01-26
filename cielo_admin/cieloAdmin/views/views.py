from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import intcomma
from ..models.service import Service
from ..models import OptionGroup, Option
from django.http import JsonResponse

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
        status = request.POST.get('status', 'active')
        image = request.FILES.get('image')
        
        # 서비스 생성
        service = Service.objects.create(
            name=name,
            description=description,
            base_price=base_price,
            status=status,
            image=image,
        )
        
        # 기본 서비스가 있다면 해당 서비스의 옵션을 복사
        default_service = Service.get_default_service()
        if default_service:
            service.clone_options_from(default_service)
        else:
            # 기본 서비스가 없는 경우 기본 옵션 그룹과 옵션을 연결
            service.option_groups.set(OptionGroup.get_default_groups())
            service.options.set(Option.get_default_options())
        
        # 사용자가 선택한 추가 옵션 연결
        group_ids = request.POST.getlist('group_ids[]')
        option_ids = request.POST.getlist('option_ids[]')
        
        if group_ids:
            service.option_groups.set(group_ids)
        if option_ids:
            service.options.set(option_ids)
        
        return redirect('cieloAdmin:service_list')
    
    # GET 요청: 폼 표시
    option_groups = OptionGroup.objects.prefetch_related('options').all()
    default_service = Service.get_default_service()
    
    context = {
        'option_groups': option_groups,
        'selected_group_ids': [],
        'selected_option_ids': [],
    }
    
    if default_service:
        context.update({
            'selected_group_ids': list(default_service.option_groups.values_list('id', flat=True)),
            'selected_option_ids': list(default_service.options.values_list('id', flat=True)),
        })
    
    return render(request, 'cieloAdmin/service/create.html', context)

def service_edit(request, service_id):
    """서비스 수정"""
    service = get_object_or_404(
        Service.objects.prefetch_related('option_groups', 'options'),
        id=service_id
    )
    
    if request.method == 'POST':
        # 기본 정보 업데이트
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.base_price = request.POST.get('base_price')
        service.status = request.POST.get('status')
        
        if 'image' in request.FILES:
            service.image = request.FILES['image']
        
        service.save()
        
        # 옵션 그룹과 옵션 연결 업데이트
        group_ids = request.POST.getlist('group_ids[]')
        option_ids = request.POST.getlist('option_ids[]')
        
        service.option_groups.set(group_ids if group_ids else [])
        service.options.set(option_ids if option_ids else [])
        
        return redirect('cieloAdmin:service_list')
    
    # GET 요청: 폼 표시
    option_groups = OptionGroup.objects.prefetch_related('options').all()
    selected_group_ids = list(service.option_groups.values_list('id', flat=True))
    selected_option_ids = list(service.options.values_list('id', flat=True))
    
    context = {
        'service': service,
        'option_groups': option_groups,
        'selected_group_ids': selected_group_ids,
        'selected_option_ids': selected_option_ids,
        'is_edit': True,
    }
    
    print("Debug - Selected Groups:", selected_group_ids)  # 디버깅용
    print("Debug - Selected Options:", selected_option_ids)  # 디버깅용
    
    return render(request, 'cieloAdmin/service/edit.html', context)

def service_delete(request, service_id):
    """서비스 삭제"""
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        service.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)

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
