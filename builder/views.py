from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from builder.models import CaseBuilder, MateBuilder, MateSeamColor, MateColor
from catalog.models import Make


def case(request):
    instance = get_object_or_404(CaseBuilder, slug='case-builder')
    context = {
        'instance': instance
    }
    return render(request, 'builder/case.html', context)


def mate(request):
    instance = get_object_or_404(MateBuilder, slug='mate-builder')
    context = {
        'instance': instance
    }
    return render(request, 'builder/mate.html', context)


@csrf_exempt
def case_initial(request):
    if request.method == 'POST':
        data = dict()
        data['makes'] = list()

        try:
            builder = CaseBuilder.objects.filter(slug='case-builder')
            data['builder'] = serialize('json', builder)

            data['cases'] = list()
            for _type in builder[0].type_set.all().order_by('order'):

                bases = list()
                for base in _type.base_set.all().order_by('order'):
                    bases.append({
                        'title': base.title,
                        'image': base.image.url,
                        'hex': base.hex,
                        'price': base.price,
                        'uuid': base.uuid
                    })

                rears = list()
                for rear in _type.rear_set.all().order_by('order'):
                    rears.append({
                        'title': rear.title,
                        'image': rear.image.url,
                        'hex': rear.hex,
                        'uuid': rear.uuid
                    })

                materials = list()
                for material in _type.material_set.all().order_by('order'):
                    colors = list()
                    for color in material.color_set.all().order_by('order'):
                        colors.append({
                            'title': color.title,
                            'image': color.image.url,
                            'hex': color.hex,
                            'uuid': color.uuid
                        })
                    materials.append({
                        'title': material.title,
                        'price': material.price,
                        'uuid': material.uuid,
                        'colors': colors
                    })

                seams = list()
                for seam in _type.seam_set.all().order_by('order'):
                    colors = list()
                    for color in seam.seamcolor_set.all().order_by('order'):
                        colors.append({
                            'title': color.title,
                            'image': color.image.url,
                            'hex': color.hex,
                            'uuid': color.uuid
                        })
                    seams.append({
                        'title': seam.title,
                        'price': seam.price,
                        'uuid': seam.uuid,
                        'colors': colors
                    })

                data['cases'].append({
                    'title': _type.title,
                    'rears': rears,
                    'bases': bases,
                    'materials': materials,
                    'seams': seams
                })

        except ObjectDoesNotExist:
            pass

        makes = Make.objects.all()
        for make in makes:
            models = make.model_set.all()
            data['makes'].append({
                'slug': make.slug,
                'title': make.title,
                'models': [{'title': model.title} for model in models]
            })

        return JsonResponse(data)
    return HttpResponseNotFound()


@csrf_exempt
def mate_initial(request):
    if request.method == 'POST':
        data = dict()
        data['makes'] = list()

        try:
            builder = MateBuilder.objects.get(slug='mate-builder')
            data['builder'] = serialize('json', [builder])

            data['colors'] = list()
            for color in builder.matecolor_set.all():
                data['colors'].append({
                    'title': color.title,
                    'image': color.image.url,
                    'uuid': color.uuid
                })

            data['seam_colors'] = list()
            for color in builder.mateseamcolor_set.all():
                data['seam_colors'].append({
                    'title': color.title,
                    'hex': color.hex,
                    'uuid': color.uuid
                })

        except ObjectDoesNotExist:
            pass

        makes = Make.objects.all()
        for make in makes:
            models = make.model_set.all()
            data['makes'].append({
                'slug': make.slug,
                'title': make.title,
                'models': [{'title': model.title} for model in models]
            })

        return JsonResponse(data)
    return HttpResponseNotFound()
