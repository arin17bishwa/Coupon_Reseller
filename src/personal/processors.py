from django.conf import settings


def hallnmeal(request):
    kwargs = {
        'HALLS': settings.HALLS,
        'MEALS': settings.MEALS
    }
    return kwargs
