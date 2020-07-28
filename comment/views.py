from django.core.mail import send_mass_mail
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render

from app import settings
from comment.forms import MainReviewForm
from comment.models import MainReviewSection, MainReview
from settings.models import Moderator


def add_review(request):
    form = MainReviewForm
    if request.user.is_authenticated:
        user = request.user
        form = form(initial={
            'name': user.full_name,
            'phone': user.phone,
            'email': user.email,
        })

    instance = {
        'title': 'Добавить отзыв',
        'content': '<p>Здесь вы можете оставить отзыв о любом товаре или услуге, специалисте или компании. <br>'
                   'Вашими рекомендациями смогут воспользоваться ваши друзья и знакомые</p>'
    }
    context = {
        'instance': instance,
        'form': form
    }
    return render(request, 'comment/add-review.html', context=context)


def add_review_action(request):
    if request.method == 'POST':
        data = dict()

        post = request.POST
        files = request.FILES
        section = MainReviewSection.objects.get(id=request.POST.get('section'))

        new_review = MainReview.objects.create(
            name=post.get('name'),
            email=post.get('email'),
            phone=post.get('phone'),
            image=files.get('image'),
            video=post.get('video'),
            content=post.get('content'),
            section=section
        )

        if new_review:
            data['success'] = True

            moderators = Moderator.objects.filter(active=True)

            if moderators.count:
                messages = ()
                for moderator in moderators:
                    message = (
                        'Новый отзыв на "avtopilot.online"',
                        '''
                        Здравствуйте, %s!
                        Пожалуйста, будьте так любезны и не откажите в чести промодерировать новый отзыв.
                        Вот ссылочка: https://%s/aristarx/comment/mainreview/%s/change/
                        ''' % (moderator.name, request.META.get('HTTP_HOST'), new_review.id),
                        settings.EMAIL_HOST_USER,
                        [moderator.email]
                    )

                    messages = list(messages)
                    messages.append(message)
                    messages = tuple(messages)

                send_mass_mail(messages, fail_silently=False)

        return JsonResponse(data)
    return HttpResponseNotFound()
