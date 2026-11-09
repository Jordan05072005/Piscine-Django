from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.template.loader import render_to_string
from .form import LoginForm


def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST only'}, status=405)

    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        login(request, form.get_user())
        html = render_to_string('logout.html', request=request)
        return JsonResponse({'success': True, 'html': html})

    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST only'}, status=405)

    logout(request)
    html = render_to_string('login.html', {'form': LoginForm()}, request=request)
    return JsonResponse({'success': True, 'html': html})