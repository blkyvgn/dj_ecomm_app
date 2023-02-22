from django.views.decorators.http import require_http_methods
from django.shortcuts import render



@require_http_methods(['GET'])
def error_404(request, *args, **kwargs):
    data = {'msg':kwargs.get('exception', None)}
    return render(request,'error/404.html', data)

@require_http_methods(['GET'])
def error_500(request, *args, **kwargs):
    data = {'msg':kwargs.get('exception', None)}
    return render(request,'error/500.html', data)

@require_http_methods(['GET'])
def error_403(request, *args, **kwargs):
    data = {'msg':kwargs.get('exception', None)}
    return render(request,'error/403.html', data)

@require_http_methods(['GET'])
def error_400(request, *args, **kwargs):
    data = {'msg':kwargs.get('exception', None)}
    return render(request,'error/400.html', data)

