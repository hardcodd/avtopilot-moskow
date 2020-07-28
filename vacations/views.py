from django.shortcuts import render

from vacations.models import Vacations


def vacations(request):
    instance = Vacations.objects.get(slug='vacations')
    context = {
        'instance': instance
    }
    return render(request, 'vacations/vacations.html', context)
