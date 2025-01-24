from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            if remember:
                # 30일 동안 세션 유지
                request.session.set_expiry(30 * 24 * 60 * 60)
            else:
                # 브라우저 종료 시 세션 만료
                request.session.set_expiry(0)
            
            return redirect('dashboard')
        else:
            messages.error(request, '이메일 또는 비밀번호가 올바르지 않습니다.')
    
    return render(request, 'cieloAdmin/login.html')
