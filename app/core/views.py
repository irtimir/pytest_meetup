from django.http import HttpResponse


def heathcheck(request):
    return HttpResponse('OK')
